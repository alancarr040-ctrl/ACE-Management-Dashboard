from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ACEConnectionProfile:
    name: str
    database: str
    host: str
    port: int
    user: str


class ACEDataService:
    """Read-only gateway for ACE database information.

    Phase 3.0 establishes ACEMD's first safe ACE data access layer.  All ACE
    database access for Administration modules should go through this service
    rather than embedding SQL in routes or templates.
    """

    READ_ONLY_PREFIXES = ("select", "show", "describe", "desc", "explain")
    MUTATING_KEYWORDS = re.compile(
        r"\b(insert|update|delete|replace|drop|alter|create|truncate|grant|revoke|set|call|load|outfile|dumpfile|lock|unlock)\b",
        re.IGNORECASE,
    )

    def __init__(self, root_path: str | Path | None = None):
        self.root_path = Path(root_path or os.environ.get("ACE_ROOT", "/opt/acserver")).resolve()
        self.env = self._load_environment()

    def get_overview(self) -> dict[str, Any]:
        profiles = self.get_profiles()
        results = [self.get_database_overview(profile.name) for profile in profiles]
        connected = sum(1 for result in results if result["connected"])
        total_tables = sum(result.get("table_count", 0) for result in results)
        total_rows = sum(result.get("total_rows", 0) for result in results)
        return {
            "configured": bool(profiles),
            "driver": self._driver_status(),
            "profiles": results,
            "summary": {
                "profiles": len(profiles),
                "connected": connected,
                "tables": total_tables,
                "rows": total_rows,
                "mode": "Read-only",
            },
            "enforcement": self.get_read_only_report(),
        }

    def get_profiles(self) -> list[ACEConnectionProfile]:
        host = self._env("ACE_SQL_AUTH_DATABASE_HOST", "ACE_DB_HOST", "MYSQL_HOST", default="ace-db")
        port = int(self._env("ACE_SQL_AUTH_DATABASE_PORT", "ACE_DB_PORT", "MYSQL_PORT", default="3306") or 3306)
        user = self._env("MYSQL_USER", "ACE_DB_USER", "DB_USER", default="")
        profiles = []
        for key, label in (
            ("ACE_SQL_AUTH_DATABASE_NAME", "Auth"),
            ("ACE_SQL_SHARD_DATABASE_NAME", "Shard"),
            ("ACE_SQL_WORLD_DATABASE_NAME", "World"),
        ):
            database = self._env(key, default="")
            if database:
                profiles.append(ACEConnectionProfile(label, database, host, port, user))
        if not profiles:
            database = self._env("MYSQL_DATABASE", "ACE_DB_NAME", "DB_NAME", default="")
            if database and "%" not in database:
                profiles.append(ACEConnectionProfile("ACE", database, host, port, user))
        return profiles

    def get_database_overview(self, profile_name: str) -> dict[str, Any]:
        profile = self._find_profile(profile_name)
        if not profile:
            return {"name": profile_name, "connected": False, "error": "Profile is not configured."}
        result = {
            "name": profile.name,
            "database": profile.database,
            "host": profile.host,
            "port": profile.port,
            "user": profile.user or "Not configured",
            "connected": False,
            "tables": [],
            "table_count": 0,
            "total_rows": 0,
            "error": None,
        }
        try:
            with self._connect(profile) as conn:
                rows = self._query(conn, """
                    SELECT table_name, table_rows, data_length, index_length
                    FROM information_schema.tables
                    WHERE table_schema = %s
                    ORDER BY table_name
                """, (profile.database,))
                tables = [
                    {
                        "name": row["table_name"],
                        "rows": int(row.get("table_rows") or 0),
                        "data_bytes": int(row.get("data_length") or 0),
                        "index_bytes": int(row.get("index_length") or 0),
                    }
                    for row in rows
                ]
                result.update({
                    "connected": True,
                    "tables": tables,
                    "table_count": len(tables),
                    "total_rows": sum(t["rows"] for t in tables),
                })
        except Exception as exc:  # pragma: no cover - depends on deployment DB
            result["error"] = str(exc)
        return result

    def get_schema_inventory(self) -> dict[str, Any]:
        overview = self.get_overview()
        return {
            "summary": overview["summary"],
            "profiles": overview["profiles"],
            "capabilities": self.get_capabilities(),
            "enforcement": overview["enforcement"],
        }

    def get_accounts(self, limit: int = 50, search: str = "") -> dict[str, Any]:
        return self._get_entity_list(
            "Auth",
            ["account", "accounts", "ace_account"],
            ["accountName", "account_name", "name", "username", "email", "id"],
            limit,
            search,
            "accounts",
        )

    def get_characters(self, limit: int = 50, search: str = "") -> dict[str, Any]:
        return self._get_entity_list(
            "Shard",
            ["character", "characters", "biota"],
            ["name", "characterName", "character_name", "id", "accountId", "account_id"],
            limit,
            search,
            "characters",
        )

    def get_world(self) -> dict[str, Any]:
        profile = self._find_profile("World")
        if not profile:
            return {"connected": False, "error": "World profile is not configured.", "tables": [], "interesting": []}
        overview = self.get_database_overview("World")
        interesting_names = ("weenie", "landblock", "landblock_instance", "treasure", "recipe", "event", "encounter")
        interesting = [t for t in overview.get("tables", []) if any(part in t["name"].lower() for part in interesting_names)]
        return {**overview, "interesting": interesting[:25]}

    def get_server_data(self) -> dict[str, Any]:
        overview = self.get_overview()
        return {
            "connection": overview["summary"],
            "profiles": overview["profiles"],
            "capabilities": self.get_capabilities(),
        }

    def get_capabilities(self) -> list[dict[str, str]]:
        return [
            {"name": "Connection discovery", "status": "Active", "description": "Reads ACE database profile settings from environment or /opt/acserver/.env."},
            {"name": "Schema inventory", "status": "Active", "description": "Uses information_schema to list databases, tables, columns, and estimated row counts."},
            {"name": "Account discovery", "status": "Active", "description": "Safely detects likely account tables and displays read-only rows when available."},
            {"name": "Character discovery", "status": "Active", "description": "Safely detects likely character tables and displays read-only rows when available."},
            {"name": "Write actions", "status": "Disabled", "description": "3.0.0 intentionally rejects mutation SQL and exposes no edit actions."},
        ]

    def get_read_only_report(self) -> dict[str, Any]:
        return {
            "mode": "Read-only",
            "allowed": list(self.READ_ONLY_PREFIXES),
            "blocked": ["INSERT", "UPDATE", "DELETE", "REPLACE", "DROP", "ALTER", "CREATE", "TRUNCATE", "GRANT", "REVOKE"],
            "templates": "No SQL is executed from templates.",
            "routes": "Administration routes consume ACEDataService only.",
        }

    def _get_entity_list(self, profile_name: str, table_candidates: list[str], search_columns: list[str], limit: int, search: str, entity: str) -> dict[str, Any]:
        profile = self._find_profile(profile_name)
        result = {"entity": entity, "connected": False, "profile": profile_name, "table": None, "columns": [], "rows": [], "total": 0, "search": search, "error": None}
        if not profile:
            result["error"] = f"{profile_name} profile is not configured."
            return result
        try:
            with self._connect(profile) as conn:
                result["connected"] = True
                table = self._detect_table(conn, profile.database, table_candidates)
                if not table:
                    result["error"] = "No expected table was detected yet. Use the Database page to inspect the schema."
                    return result
                columns = self._get_columns(conn, profile.database, table)
                result["table"] = table
                result["columns"] = columns
                selected_columns = columns[:10]
                where = ""
                params: list[Any] = []
                searchable = [c for c in columns if c in search_columns]
                if search and searchable:
                    where = " WHERE " + " OR ".join(f"`{c}` LIKE %s" for c in searchable[:4])
                    params = [f"%{search}%" for _ in searchable[:4]]
                count_rows = self._query(conn, f"SELECT COUNT(*) AS row_count FROM `{profile.database}`.`{table}`{where}", tuple(params))
                result["total"] = int(count_rows[0].get("row_count") or 0) if count_rows else 0
                sql = f"SELECT {', '.join(f'`{c}`' for c in selected_columns)} FROM `{profile.database}`.`{table}`{where} LIMIT %s"
                rows = self._query(conn, sql, tuple(params + [max(1, min(int(limit), 200))]))
                result["rows"] = [{c: row.get(c) for c in selected_columns} for row in rows]
        except Exception as exc:  # pragma: no cover - depends on deployment DB
            result["error"] = str(exc)
        return result

    def _detect_table(self, conn: Any, database: str, candidates: list[str]) -> str | None:
        rows = self._query(conn, "SELECT table_name FROM information_schema.tables WHERE table_schema = %s", (database,))
        tables = [row["table_name"] for row in rows]
        lower_map = {table.lower(): table for table in tables}
        for candidate in candidates:
            if candidate.lower() in lower_map:
                return lower_map[candidate.lower()]
        for table in tables:
            table_lower = table.lower()
            if any(candidate.lower() in table_lower for candidate in candidates):
                return table
        return None

    def _get_columns(self, conn: Any, database: str, table: str) -> list[str]:
        rows = self._query(conn, """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
        """, (database, table))
        return [row["column_name"] for row in rows]

    def _find_profile(self, profile_name: str) -> ACEConnectionProfile | None:
        profile_name = profile_name.lower()
        for profile in self.get_profiles():
            if profile.name.lower() == profile_name or profile.database.lower() == profile_name:
                return profile
        return None

    def _connect(self, profile: ACEConnectionProfile):
        try:
            import pymysql
        except Exception as exc:  # pragma: no cover - import depends on deployment image
            raise RuntimeError("PyMySQL is not installed. Install dashboard requirements to enable ACE DB read-only access.") from exc
        password = self._env("MYSQL_PASSWORD", "ACE_DB_PASSWORD", "DB_PASS", "DB_PASSWORD", default="")
        return pymysql.connect(
            host=profile.host,
            port=profile.port,
            user=profile.user,
            password=password,
            database=profile.database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            read_timeout=5,
            write_timeout=5,
            connect_timeout=5,
            autocommit=True,
        )

    def _query(self, conn: Any, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        self._assert_read_only(sql)
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return list(cursor.fetchall())

    def _assert_read_only(self, sql: str) -> None:
        cleaned = sql.strip().lower()
        if ";" in cleaned.rstrip(";"):
            raise ValueError("Multiple SQL statements are not allowed.")
        if not cleaned.startswith(self.READ_ONLY_PREFIXES):
            raise ValueError("Only read-only SQL statements are allowed.")
        if self.MUTATING_KEYWORDS.search(cleaned):
            raise ValueError("Mutation SQL is blocked by ACEDataService read-only enforcement.")

    def _load_environment(self) -> dict[str, str]:
        env = dict(os.environ)
        for path in (self.root_path / ".env", Path.cwd() / ".env"):
            if path.exists():
                env.update(self._parse_env_file(path))
        return env

    def _parse_env_file(self, path: Path) -> dict[str, str]:
        values: dict[str, str] = {}
        for raw_line in path.read_text(errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
        return values

    def _env(self, *keys: str, default: str = "") -> str:
        for key in keys:
            value = self.env.get(key)
            if value not in (None, ""):
                return str(value)
        return default

    def _driver_status(self) -> dict[str, str]:
        try:
            import pymysql  # noqa: F401
            return {"name": "PyMySQL", "status": "Available"}
        except Exception:
            return {"name": "PyMySQL", "status": "Missing"}
