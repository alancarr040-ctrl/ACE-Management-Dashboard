#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="${1:-/opt/acserver}"
DOCKER_SOCKET="${DOCKER_SOCKET:-/var/run/docker.sock}"
ENV_FILE="$BASE_DIR/.env"
DATA_DIR="$BASE_DIR/data"
RUNTIME_DIR="$BASE_DIR/backups/runtime"

PERSISTENT_DIRS=(
  research_lab
  research_lab/snapshots
  registry
  knowledge
  screenshots
  imports
  exports
  cache
  logs
)

if [ "${EUID:-$(id -u)}" -ne 0 ]; then
  command -v sudo >/dev/null 2>&1 || { echo "ERROR: Root privilege is required to repair inherited ownership, and sudo is unavailable." >&2; exit 2; }
  exec sudo --preserve-env=DOCKER_SOCKET "$0" "$BASE_DIR"
fi

fail() {
  echo "ERROR: $*" >&2
  exit 2
}

warn() {
  echo "WARNING: $*" >&2
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

upsert_env() {
  local key="$1" value="$2" tmp
  tmp="$(mktemp "${ENV_FILE}.XXXXXX")"
  awk -v key="$key" -v value="$value" '
    BEGIN { found=0 }
    $0 ~ "^[[:space:]]*" key "=" {
      if (!found) print key "=" value
      found=1
      next
    }
    { print }
    END { if (!found) print key "=" value }
  ' "$ENV_FILE" > "$tmp"
  chmod --reference="$ENV_FILE" "$tmp" 2>/dev/null || chmod 600 "$tmp"
  mv "$tmp" "$ENV_FILE"
}

require_command stat
require_command awk
require_command find
require_command mktemp
require_command setpriv

[ -d "$BASE_DIR" ] || fail "ACE server root does not exist: $BASE_DIR"
[ -e "$DOCKER_SOCKET" ] || fail "Docker socket not found: $DOCKER_SOCKET"
[ -S "$DOCKER_SOCKET" ] || fail "Docker socket path is not a Unix socket: $DOCKER_SOCKET"

OWNER_PAIR="$(stat -c '%u:%g' "$BASE_DIR")" || fail "Unable to inspect deployment ownership"
OWNER_UID="${OWNER_PAIR%%:*}"
OWNER_GID="${OWNER_PAIR##*:}"
DOCKER_GID="$(stat -c '%g' "$DOCKER_SOCKET")" || fail "Unable to inspect Docker socket group"

[[ "$OWNER_UID" =~ ^[0-9]+$ ]] || fail "Detected invalid deployment UID: $OWNER_UID"
[[ "$OWNER_GID" =~ ^[0-9]+$ ]] || fail "Detected invalid deployment GID: $OWNER_GID"
[[ "$DOCKER_GID" =~ ^[0-9]+$ ]] || fail "Detected invalid Docker socket GID: $DOCKER_GID"

if [ ! -e "$ENV_FILE" ]; then
  (umask 077 && : > "$ENV_FILE") || fail "Unable to create $ENV_FILE"
elif [ ! -f "$ENV_FILE" ]; then
  fail "Environment path is not a regular file: $ENV_FILE"
fi

for relative_dir in "${PERSISTENT_DIRS[@]}"; do
  mkdir -p "$DATA_DIR/$relative_dir"
done
mkdir -p "$RUNTIME_DIR"

OBSERVATIONS_FILE="$DATA_DIR/research_lab/observations.json"
RESEARCH_README="$DATA_DIR/research_lab/README.md"

if [ ! -f "$OBSERVATIONS_FILE" ]; then
  printf '[]\n' > "$OBSERVATIONS_FILE"
fi

if [ ! -f "$RESEARCH_README" ]; then
  cat > "$RESEARCH_README" <<'README'
# ACEMD Research Lab Data

This directory contains persistent ACE Management Dashboard research evidence.
It is mounted into the dashboard container and must survive image rebuilds,
container recreation, and application restarts. Do not remove it during an
application deployment.
README
fi

# ACEMD currently has two writable host trees. The permanent application-data
# root is canonical. backups/runtime remains a compatibility location for the
# existing Automation and Notifications state until those subsystems migrate.
WRITABLE_ROOTS=(
  "$DATA_DIR"
  "$RUNTIME_DIR"
)

for writable_root in "${WRITABLE_ROOTS[@]}"; do
  chown -R "$OWNER_UID:$OWNER_GID" "$writable_root" \
    || fail "Unable to normalize ownership under $writable_root"
  find "$writable_root" -type d -exec chmod 770 {} + \
    || fail "Unable to repair directory modes under $writable_root"
  find "$writable_root" -type f -exec chmod 660 {} + \
    || fail "Unable to repair file modes under $writable_root"
done
upsert_env ACEMD_UID "$OWNER_UID"
upsert_env ACEMD_GID "$OWNER_GID"
upsert_env ACEMD_DOCKER_GID "$DOCKER_GID"
chown "$OWNER_UID:$OWNER_GID" "$ENV_FILE" || fail "Unable to set .env ownership"
chmod 600 "$ENV_FILE" || fail "Unable to set mode 600 on $ENV_FILE"

# Validate the exact values written, data-tree writability, and Compose
# interpolation. These checks make the script safe to use as deployment
# preflight rather than merely as a setup convenience.
for expected in \
  "ACEMD_UID=$OWNER_UID" \
  "ACEMD_GID=$OWNER_GID" \
  "ACEMD_DOCKER_GID=$DOCKER_GID"; do
  grep -qxF "$expected" "$ENV_FILE" || fail "Environment validation failed for ${expected%%=*}"
done

for relative_dir in "${PERSISTENT_DIRS[@]}"; do
  [ -d "$DATA_DIR/$relative_dir" ] || fail "Persistent directory missing after preparation: data/$relative_dir"
done

owner_can_write() {
  setpriv --reuid "$OWNER_UID" --regid "$OWNER_GID" --clear-groups test -w "$1"
}

owner_can_write "$DATA_DIR/research_lab" \
  || fail "Research Lab storage is not writable by the deployment account: $DATA_DIR/research_lab"
owner_can_write "$OBSERVATIONS_FILE" \
  || fail "Research Lab observations file is not writable: $OBSERVATIONS_FILE"
owner_can_write "$RUNTIME_DIR" \
  || fail "Legacy runtime state directory is not writable: $RUNTIME_DIR"

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  (
    cd "$BASE_DIR"
    docker compose config >/dev/null
  ) || fail "docker compose config validation failed"
else
  warn "Docker Compose was not available; Compose interpolation validation was skipped."
fi

for writable_root in "${WRITABLE_ROOTS[@]}"; do
  remaining_foreign="$(find "$writable_root" -xdev \( ! -uid "$OWNER_UID" -o ! -gid "$OWNER_GID" \) -print -quit 2>/dev/null || true)"
  if [ -n "$remaining_foreign" ]; then
    fail "Writable storage still contains ownership that does not match ${OWNER_UID}:${OWNER_GID}: $remaining_foreign"
  fi
done

echo "ACE Management Dashboard deployment ownership is prepared."
echo "Project root     : $BASE_DIR"
echo "Dashboard UID    : $OWNER_UID"
echo "Dashboard GID    : $OWNER_GID"
echo "Docker socket GID: $DOCKER_GID"
echo "Persistent root  : $DATA_DIR"
echo "Runtime state    : $RUNTIME_DIR"
echo "Validation       : PASS"
echo
echo "Recreate the dashboard with:"
echo "  cd '$BASE_DIR' && docker compose up -d --build --force-recreate ace-dashboard"
