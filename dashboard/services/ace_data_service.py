from __future__ import annotations

import os
import socket
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import pymysql
    from pymysql.cursors import DictCursor
except Exception:  # pragma: no cover - dependency may not exist in local lint sandbox
    pymysql = None
    DictCursor = None


@dataclass(frozen=True)
class ACEDatabaseProfile:
    key: str
    label: str
    database: str
    host: str
    port: int
    user: str
    password: str


class ACEDataService:
    """Read-only gateway for ACE data.

    ACEMD pages must consume ACE data through this service rather than issuing
    ad-hoc SQL. Phase 3.0.1 intentionally provides discovery and explorer
    methods only. Mutation SQL is rejected by the query guard.
    """

    DEFAULT_ENV_FILES = (
        "/opt/acserver/.env",
        "/opt/acserver/docker.env",
        ".env",
        "docker.env",
    )

    SAFE_SQL_PREFIXES = ("select", "show", "describe", "desc", "explain")
    BLOCKED_SQL_WORDS = (
        "insert", "update", "delete", "replace", "alter", "drop", "create",
        "truncate", "rename", "grant", "revoke", "lock", "unlock", "set",
        "call", "load", "outfile", "infile",
    )

    SCHEMA_BASELINE = {
        "ace_auth": {
            "label": "Auth",
            "role": "Identity and game access levels",
            "tables": ("accesslevel", "account"),
            "known_core": ("account", "accesslevel"),
        },
        "ace_shard": {
            "label": "Shard",
            "role": "Runtime shard objects, characters, and dynamic properties",
            "tables": (
                "biota", "biota_properties_allegiance", "biota_properties_anim_part",
                "biota_properties_attribute", "biota_properties_attribute_2nd",
                "biota_properties_body_part", "biota_properties_book",
                "biota_properties_book_page_data", "biota_properties_bool",
                "biota_properties_create_list", "biota_properties_d_i_d",
                "biota_properties_emote", "biota_properties_emote_action",
                "biota_properties_enchantment_registry", "biota_properties_event_filter",
                "biota_properties_float", "biota_properties_generator", "biota_properties_i_i_d",
                "biota_properties_int", "biota_properties_int64", "biota_properties_palette",
                "biota_properties_position", "biota_properties_skill", "biota_properties_spell_book",
                "biota_properties_string", "biota_properties_texture_map", "character",
                "character_properties_contract_registry", "character_properties_fill_comp_book",
                "character_properties_friend_list", "character_properties_quest_registry",
                "character_properties_shortcut_bar", "character_properties_spell_bar",
                "character_properties_squelch", "character_properties_title_book",
                "config_properties_boolean", "config_properties_double", "config_properties_long",
                "config_properties_string", "house_permission",
            ),
            "known_core": ("character", "biota"),
        },
        "ace_world": {
            "label": "World",
            "role": "Static world content, weenies, encounters, quests, and recipes",
            "tables": (
                "cook_book", "encounter", "event", "house_portal", "landblock_instance",
                "landblock_instance_link", "points_of_interest", "quest", "recipe", "recipe_mod",
                "recipe_mods_bool", "recipe_mods_d_i_d", "recipe_mods_float", "recipe_mods_i_i_d",
                "recipe_mods_int", "recipe_mods_string", "recipe_requirements_bool",
                "recipe_requirements_d_i_d", "recipe_requirements_float", "recipe_requirements_i_i_d",
                "recipe_requirements_int", "recipe_requirements_string", "spell", "treasure_death",
                "treasure_gem_count", "treasure_material_base", "treasure_material_color",
                "treasure_material_groups", "treasure_wielded", "version", "weenie",
                "weenie_properties_anim_part", "weenie_properties_attribute",
                "weenie_properties_attribute_2nd", "weenie_properties_body_part",
                "weenie_properties_book", "weenie_properties_book_page_data",
                "weenie_properties_bool", "weenie_properties_create_list", "weenie_properties_d_i_d",
                "weenie_properties_emote", "weenie_properties_emote_action",
                "weenie_properties_event_filter", "weenie_properties_float",
                "weenie_properties_generator", "weenie_properties_i_i_d", "weenie_properties_int",
                "weenie_properties_int64", "weenie_properties_palette", "weenie_properties_position",
                "weenie_properties_skill", "weenie_properties_spell_book", "weenie_properties_string",
                "weenie_properties_texture_map",
            ),
            "known_core": ("weenie", "landblock_instance", "quest", "encounter", "recipe"),
        },
    }

    def __init__(self, env_files: tuple[str, ...] | None = None):
        self.env_files = env_files or self.DEFAULT_ENV_FILES
        self._env = self._load_env()

    def get_overview(self) -> dict[str, Any]:
        profiles = self.get_profiles()
        profile_reports = [self.get_profile_report(profile) for profile in profiles]
        connected = sum(1 for p in profile_reports if p["status"] == "Connected")
        tables = sum(p.get("table_count", 0) for p in profile_reports)
        rows = sum(p.get("estimated_rows", 0) for p in profile_reports)
        return {
            "profiles": profile_reports,
            "summary": {
                "profiles": len(profile_reports),
                "connected": connected,
                "tables": tables,
                "rows": rows,
                "mode": "Read-only",
                "dependency": "PyMySQL" if pymysql else "PyMySQL missing",
            },
            "capabilities": self.get_capabilities(),
        }

    def get_profiles(self) -> list[ACEDatabaseProfile]:
        host = self._env_value("ACE_SQL_DATABASE_HOST", "MYSQL_HOST", default="ace-db")
        port = int(self._env_value("ACE_SQL_DATABASE_PORT", "MYSQL_PORT", default="3306") or 3306)
        user = self._env_value("ACE_SQL_DATABASE_USER", "MYSQL_USER", default="")
        password = self._env_value("ACE_SQL_DATABASE_PASSWORD", "MYSQL_PASSWORD", default="")
        defaults = {
            "auth": ("Auth", "ACE_SQL_AUTH_DATABASE_NAME", "ace_auth"),
            "shard": ("Shard", "ACE_SQL_SHARD_DATABASE_NAME", "ace_shard"),
            "world": ("World", "ACE_SQL_WORLD_DATABASE_NAME", "ace_world"),
        }
        profiles: list[ACEDatabaseProfile] = []
        for key, (label, db_var, fallback_db) in defaults.items():
            profiles.append(ACEDatabaseProfile(
                key=key,
                label=label,
                database=self._env_value(db_var, default=fallback_db),
                host=self._env_value(f"ACE_SQL_{key.upper()}_DATABASE_HOST", default=host),
                port=int(self._env_value(f"ACE_SQL_{key.upper()}_DATABASE_PORT", default=str(port)) or port),
                user=self._env_value(f"ACE_SQL_{key.upper()}_DATABASE_USER", default=user),
                password=self._env_value(f"ACE_SQL_{key.upper()}_DATABASE_PASSWORD", default=password),
            ))
        return profiles

    @staticmethod
    def _row_value(row: dict[str, Any], *keys: str, default: Any = None) -> Any:
        """Return a dict value while tolerating MySQL driver key casing.

        MariaDB/MySQL information_schema columns may be returned as either
        table_name or TABLE_NAME depending on server and driver behavior. The
        UI consumes normalized service keys only, so all normalization stays here.
        """
        for key in keys:
            if key in row:
                return row[key]
            lower = key.lower()
            upper = key.upper()
            if lower in row:
                return row[lower]
            if upper in row:
                return row[upper]
        return default

    @staticmethod
    def _bit_bool(value: Any) -> bool:
        if isinstance(value, (bytes, bytearray)):
            return any(value)
        return bool(value)

    @staticmethod
    def _safe_identifier(value: str) -> str:
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        if not value or any(ch not in allowed for ch in value):
            raise ValueError("Unsafe ACE database identifier rejected.")
        return value

    def get_profile_report(self, profile: ACEDatabaseProfile) -> dict[str, Any]:
        baseline = self._baseline_for_database(profile.database)
        report = {
            "key": profile.key,
            "label": profile.label,
            "database": profile.database,
            "host": f"{profile.host}:{profile.port}",
            "user": profile.user or "Not configured",
            "status": "Unavailable",
            "error": "",
            "table_count": 0,
            "estimated_rows": 0,
            "role": baseline.get("role", "ACE database"),
            "baseline_tables": len(baseline.get("tables", ())),
        }
        if not pymysql:
            report["error"] = "PyMySQL dependency is not installed in the dashboard container."
            return report
        if not profile.user or not profile.password:
            report["error"] = "Database user/password not found in environment."
            return report
        try:
            rows = self._select(profile, """
                SELECT table_name, table_rows
                FROM information_schema.tables
                WHERE table_schema = %s
                ORDER BY table_name
            """, (profile.database,))
            report["status"] = "Connected"
            report["table_count"] = len(rows)
            report["estimated_rows"] = int(sum(int(self._row_value(r, "table_rows", "TABLE_ROWS", default=0) or 0) for r in rows))
        except Exception as exc:
            report["error"] = self._safe_error(exc)
        return report

    def get_schema_inventory(self) -> dict[str, Any]:
        inventories = []
        for profile in self.get_profiles():
            baseline = self._baseline_for_database(profile.database)
            entry = {
                "profile": profile.label,
                "key": profile.key,
                "database": profile.database,
                "role": baseline.get("role", "ACE database"),
                "status": "Unavailable",
                "tables": [],
                "error": "",
            }
            if pymysql and profile.user and profile.password:
                try:
                    rows = self._select(profile, """
                        SELECT table_name, table_rows, engine, table_comment
                        FROM information_schema.tables
                        WHERE table_schema = %s
                        ORDER BY table_name
                    """, (profile.database,))
                    entry["status"] = "Connected"
                    entry["tables"] = [
                        {
                            "name": self._row_value(r, "table_name", "TABLE_NAME", default=""),
                            "rows": int(self._row_value(r, "table_rows", "TABLE_ROWS", default=0) or 0),
                            "engine": self._row_value(r, "engine", "ENGINE", default="") or "",
                            "comment": self._row_value(r, "table_comment", "TABLE_COMMENT", default="") or "",
                            "core": self._row_value(r, "table_name", "TABLE_NAME", default="") in baseline.get("known_core", ()),
                        }
                        for r in rows
                    ]
                except Exception as exc:
                    entry["error"] = self._safe_error(exc)
            else:
                entry["tables"] = [
                    {"name": t, "rows": None, "engine": "", "comment": "Known from baseline SQL dump", "core": t in baseline.get("known_core", ())}
                    for t in baseline.get("tables", ())
                ]
                entry["error"] = "Using documented baseline; live connection unavailable."
            inventories.append(entry)
        return {"inventories": inventories}

    def get_accounts(self, search: str = "", limit: int = 50) -> dict[str, Any]:
        profile = self._profile("auth")
        result = {"status": "Unavailable", "rows": [], "error": "", "count": 0}
        if not self._can_connect(profile):
            result["error"] = "Live ACE auth database connection unavailable."
            return result
        try:
            where = ""
            params: list[Any] = []
            if search:
                where = "WHERE a.accountName LIKE %s OR CAST(a.accountId AS CHAR) = %s"
                params.extend([f"%{search}%", search])
            shard_db = self._safe_identifier(self._profile("shard").database)
            sql = f"""
                SELECT a.accountId, a.accountName, a.accessLevel, al.name AS accessLevelName,
                       a.email_Address, a.create_Time, a.last_Login_Time,
                       a.total_Times_Logged_In, a.banned_Time, a.ban_Expire_Time,
                       (SELECT COUNT(*) FROM `{shard_db}`.`character` c WHERE c.account_Id = a.accountId AND c.is_Deleted = 0) AS character_Count
                FROM account a
                LEFT JOIN accesslevel al ON al.level = a.accessLevel
                {where}
                ORDER BY a.accountId ASC
                LIMIT %s
            """
            params.append(limit)
            rows = self._select(profile, sql, tuple(params))
            result.update({"status": "Connected", "rows": rows, "count": len(rows)})
        except Exception as exc:
            result["error"] = self._safe_error(exc)
        return result

    def get_characters(self, search: str = "", limit: int = 50) -> dict[str, Any]:
        profile = self._profile("shard")
        result = {"status": "Unavailable", "rows": [], "error": "", "count": 0}
        if not self._can_connect(profile):
            result["error"] = "Live ACE shard database connection unavailable."
            return result
        try:
            where = ""
            params: list[Any] = []
            if search:
                where = "WHERE c.name LIKE %s OR CAST(c.id AS CHAR) = %s OR CAST(c.account_Id AS CHAR) = %s"
                params.extend([f"%{search}%", search, search])
            auth_db = self._safe_identifier(self._profile("auth").database)
            sql = f"""
                SELECT c.id, c.account_Id, a.accountName, c.name, c.is_Plussed, c.is_Deleted,
                       c.last_Login_Timestamp, c.total_Logins, b.weenie_Class_Id, b.weenie_Type
                FROM `character` c
                LEFT JOIN biota b ON b.id = c.id
                LEFT JOIN `{auth_db}`.`account` a ON a.accountId = c.account_Id
                {where}
                ORDER BY c.name ASC
                LIMIT %s
            """
            params.append(limit)
            rows = self._select(profile, sql, tuple(params))
            for row in rows:
                row["is_Plussed"] = self._bit_bool(row.get("is_Plussed"))
                row["is_Deleted"] = self._bit_bool(row.get("is_Deleted"))
            result.update({"status": "Connected", "rows": rows, "count": len(rows)})
        except Exception as exc:
            result["error"] = self._safe_error(exc)
        return result


    def get_account_detail(self, account_id: int) -> dict[str, Any]:
        """Return one ACE account with linked characters, read-only."""
        profile = self._profile("auth")
        result = {"status": "Unavailable", "account": None, "characters": [], "error": ""}
        if not self._can_connect(profile):
            result["error"] = "Live ACE auth database connection unavailable."
            return result
        try:
            account_columns = self._table_columns(profile, "account")
            optional_select = ",\n                       ".join([
                self._optional_column_expr(account_columns, "a", "email_Address"),
                self._optional_column_expr(account_columns, "a", "create_Time"),
                self._optional_column_expr(account_columns, "a", "last_Login_Time"),
                self._optional_column_expr(account_columns, "a", "total_Times_Logged_In", "0"),
                self._optional_column_expr(account_columns, "a", "banned_Time"),
                self._optional_column_expr(account_columns, "a", "ban_Expire_Time"),
                self._optional_column_expr(account_columns, "a", "last_Login_IP"),
                self._optional_column_expr(account_columns, "a", "last_Login_Timestamp"),
            ])
            rows = self._select(profile, f"""
                SELECT a.accountId, a.accountName, a.accessLevel, al.name AS accessLevelName,
                       {optional_select}
                FROM account a
                LEFT JOIN accesslevel al ON al.level = a.accessLevel
                WHERE a.accountId = %s
                LIMIT 1
            """, (account_id,))
            result["status"] = "Connected"
            result["account"] = rows[0] if rows else None
            shard_profile = self._profile("shard")
            if result["account"] and self._can_connect(shard_profile):
                result["characters"] = self._select(shard_profile, """
                    SELECT c.id, c.name, c.is_Deleted, c.last_Login_Timestamp, c.total_Logins,
                           b.weenie_Class_Id, b.weenie_Type
                    FROM `character` c
                    LEFT JOIN biota b ON b.id = c.id
                    WHERE c.account_Id = %s
                    ORDER BY c.name ASC
                """, (account_id,))
                for row in result["characters"]:
                    row["is_Deleted"] = self._bit_bool(row.get("is_Deleted"))
        except Exception as exc:
            result["error"] = self._safe_error(exc)
        return result

    def get_character_detail(self, character_id: int) -> dict[str, Any]:
        """Return one shard character with representative read-only property rows."""
        profile = self._profile("shard")
        result = {"status": "Unavailable", "character": None, "properties": {}, "error": ""}
        if not self._can_connect(profile):
            result["error"] = "Live ACE shard database connection unavailable."
            return result
        try:
            auth_db = self._safe_identifier(self._profile("auth").database)
            rows = self._select(profile, f"""
                SELECT c.id, c.account_Id, a.accountName, c.name, c.is_Plussed, c.is_Deleted,
                       c.last_Login_Timestamp, c.total_Logins, b.weenie_Class_Id, b.weenie_Type
                FROM `character` c
                LEFT JOIN biota b ON b.id = c.id
                LEFT JOIN `{auth_db}`.`account` a ON a.accountId = c.account_Id
                WHERE c.id = %s
                LIMIT 1
            """, (character_id,))
            result["status"] = "Connected"
            result["character"] = rows[0] if rows else None
            if result["character"]:
                result["character"]["is_Plussed"] = self._bit_bool(result["character"].get("is_Plussed"))
                result["character"]["is_Deleted"] = self._bit_bool(result["character"].get("is_Deleted"))
                for key, table, value_col in (
                    ("ints", "biota_properties_int", "value"),
                    ("strings", "biota_properties_string", "value"),
                    ("floats", "biota_properties_float", "value"),
                    ("bools", "biota_properties_bool", "value"),
                    ("positions", "biota_properties_position", "obj_Cell_Id"),
                    ("dids", "biota_properties_d_i_d", "value"),
                    ("iids", "biota_properties_i_i_d", "value"),
                ):
                    if self._table_exists(profile, table):
                        try:
                            rows = self._select(profile, f"SELECT * FROM `{table}` WHERE object_Id = %s ORDER BY `type` ASC LIMIT 25", (character_id,))
                            result["properties"][key] = rows
                        except Exception:
                            result["properties"][key] = []
        except Exception as exc:
            result["error"] = self._safe_error(exc)
        return result

    def get_table_detail(self, database_key: str, table_name: str) -> dict[str, Any]:
        """Return schema details for a single ACE table, read-only."""
        profile = self._profile(database_key)
        table_name = self._safe_identifier(table_name)
        result = {"status": "Unavailable", "database_key": database_key, "database": profile.database, "table": table_name, "columns": [], "indexes": [], "sample": [], "row_count": None, "error": ""}
        if not self._can_connect(profile):
            result["error"] = "Live ACE database connection unavailable."
            return result
        try:
            if not self._table_exists(profile, table_name):
                result["status"] = "Connected"
                result["error"] = "Table was not found in the selected ACE database."
                return result
            result["status"] = "Connected"
            column_rows = self._select(profile, """
                SELECT column_name, column_type, is_nullable, column_key, column_default, extra, column_comment
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
            """, (profile.database, table_name))
            result["columns"] = [
                {
                    "column_name": self._row_value(row, "column_name", "COLUMN_NAME", default=""),
                    "column_type": self._row_value(row, "column_type", "COLUMN_TYPE", default=""),
                    "is_nullable": self._row_value(row, "is_nullable", "IS_NULLABLE", default=""),
                    "column_key": self._row_value(row, "column_key", "COLUMN_KEY", default=""),
                    "column_default": self._row_value(row, "column_default", "COLUMN_DEFAULT", default=""),
                    "extra": self._row_value(row, "extra", "EXTRA", default=""),
                    "column_comment": self._row_value(row, "column_comment", "COLUMN_COMMENT", default=""),
                }
                for row in column_rows
            ]
            index_rows = self._select(profile, """
                SELECT index_name, non_unique, seq_in_index, column_name, index_type
                FROM information_schema.statistics
                WHERE table_schema = %s AND table_name = %s
                ORDER BY index_name, seq_in_index
            """, (profile.database, table_name))
            result["indexes"] = [
                {
                    "index_name": self._row_value(row, "index_name", "INDEX_NAME", default=""),
                    "non_unique": self._row_value(row, "non_unique", "NON_UNIQUE", default=0),
                    "seq_in_index": self._row_value(row, "seq_in_index", "SEQ_IN_INDEX", default=""),
                    "column_name": self._row_value(row, "column_name", "COLUMN_NAME", default=""),
                    "index_type": self._row_value(row, "index_type", "INDEX_TYPE", default=""),
                }
                for row in index_rows
            ]
            count_rows = self._select(profile, f"SELECT COUNT(*) AS count_value FROM `{table_name}`", ())
            result["row_count"] = int(count_rows[0].get("count_value") or 0) if count_rows else 0
            sample_rows = self._select(profile, f"SELECT * FROM `{table_name}` LIMIT 10", ())
            result["sample"] = [self._redact_sensitive_row(row) for row in sample_rows]
        except Exception as exc:
            result["error"] = self._safe_error(exc)
        return result

    def get_world_summary(self) -> dict[str, Any]:
        profile = self._profile("world")
        core_tables = ("weenie", "landblock_instance", "encounter", "quest", "recipe", "spell")
        result = {"status": "Unavailable", "rows": [], "error": ""}
        if not self._can_connect(profile):
            baseline = self._baseline_for_database(profile.database)
            result["rows"] = [{"table": t, "rows": None, "note": "Known baseline table"} for t in baseline.get("known_core", core_tables)]
            result["error"] = "Using documented baseline; live ACE world connection unavailable."
            return result
        try:
            rows = []
            for table in core_tables:
                if self._table_exists(profile, table):
                    count = self._select(profile, f"SELECT COUNT(*) AS count_value FROM `{table}`", ())
                    rows.append({"table": table, "rows": int(count[0].get("count_value") or 0), "note": "Live count"})
            result.update({"status": "Connected", "rows": rows})
        except Exception as exc:
            result["error"] = self._safe_error(exc)
        return result

    def get_capabilities(self) -> list[dict[str, str]]:
        return [
            {"name": "Schema baseline", "status": "Active", "detail": "Documents the known ACE auth, shard, and world schema from the initialization dump."},
            {"name": "Connection discovery", "status": "Active", "detail": "Reads ACE database settings from environment files without exposing secrets."},
            {"name": "Live schema inventory", "status": "Active", "detail": "Uses information_schema through guarded read-only SELECT statements when available."},
            {"name": "Account explorer", "status": "Read-only", "detail": "Lists account identity, access level, login metadata, and ban lifecycle fields."},
            {"name": "Character explorer", "status": "Read-only", "detail": "Lists shard characters and their linked biota metadata without mutation actions."},
            {"name": "World explorer", "status": "Read-only", "detail": "Summarizes core world tables and safe counts."},
            {"name": "Write actions", "status": "Disabled", "detail": "Mutation SQL is rejected by the ACE Data Service guard."},
        ]

    @staticmethod
    def _redact_sensitive_row(row: dict[str, Any]) -> dict[str, Any]:
        sensitive_markers = ("password", "passwd", "pwd", "salt", "hash", "token", "secret")
        clean: dict[str, Any] = {}
        for key, value in row.items():
            if any(marker in str(key).lower() for marker in sensitive_markers):
                clean[key] = "[redacted]"
            else:
                clean[key] = value
        return clean

    def _select(self, profile: ACEDatabaseProfile, sql: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
        self._guard_read_only(sql)
        with pymysql.connect(
            host=profile.host,
            port=profile.port,
            user=profile.user,
            password=profile.password,
            database=profile.database,
            charset="utf8mb4",
            cursorclass=DictCursor,
            read_timeout=4,
            write_timeout=4,
            connect_timeout=4,
            autocommit=True,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return list(cursor.fetchall())

    def _guard_read_only(self, sql: str) -> None:
        normalized = " ".join(sql.strip().lower().split())
        if not normalized.startswith(self.SAFE_SQL_PREFIXES):
            raise ValueError("ACE Data Service permits read-only SQL only.")
        padded = f" {normalized} "
        for word in self.BLOCKED_SQL_WORDS:
            if f" {word} " in padded:
                raise ValueError(f"Mutation keyword rejected by read-only guard: {word}")


    def _table_columns(self, profile: ACEDatabaseProfile, table: str) -> set[str]:
        """Return available column names for a table, normalized to lower-case."""
        table = self._safe_identifier(table)
        rows = self._select(profile, """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
        """, (profile.database, table))
        return {str(self._row_value(row, "column_name", "COLUMN_NAME", default="")).lower() for row in rows}

    @staticmethod
    def _optional_column_expr(available_columns: set[str], alias: str, column: str, default: str = "NULL") -> str:
        """Build a SELECT expression that tolerates ACE schema column differences."""
        if column.lower() in available_columns:
            return f"{alias}.`{column}` AS `{column}`"
        return f"{default} AS `{column}`"

    def _table_exists(self, profile: ACEDatabaseProfile, table: str) -> bool:
        rows = self._select(profile, """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
            LIMIT 1
        """, (profile.database, table))
        return bool(rows)

    def _can_connect(self, profile: ACEDatabaseProfile) -> bool:
        return bool(pymysql and profile.user and profile.password)

    def _profile(self, key: str) -> ACEDatabaseProfile:
        for profile in self.get_profiles():
            if profile.key == key:
                return profile
        raise KeyError(key)

    def _baseline_for_database(self, database: str) -> dict[str, Any]:
        return self.SCHEMA_BASELINE.get(database, {"tables": (), "known_core": (), "role": "ACE database"})

    def _env_value(self, *keys: str, default: str = "") -> str:
        for key in keys:
            value = os.environ.get(key)
            if value:
                return value
            value = self._env.get(key)
            if value:
                return value
        return default

    def _load_env(self) -> dict[str, str]:
        env: dict[str, str] = {}
        for env_file in self.env_files:
            path = Path(env_file)
            if not path.exists():
                continue
            try:
                for raw in path.read_text(errors="ignore").splitlines():
                    line = raw.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    env[key.strip()] = value.strip().strip('"').strip("'")
            except OSError:
                continue
        return env

    def _safe_error(self, exc: Exception) -> str:
        text = str(exc)
        for profile in self.get_profiles():
            if profile.password:
                text = text.replace(profile.password, "********")
        return text[:500]
