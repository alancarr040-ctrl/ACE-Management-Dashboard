#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="${ACEMD_BASE_DIR:-/opt/acserver}"
BACKUP_ROOT="$BASE_DIR/backups/runtime"
STAMP="$(date +%Y-%m-%d_%H-%M-%S)"
BACKUP_DIR="$BACKUP_ROOT/$STAMP"
JOB_START="$(date +%s)"

REQUIRED_PATHS=(
  "docker-compose.yml"
  ".env"
  "ace/Config"
  "data"
  "scripts"
)

OPTIONAL_PATHS=(
  "README.md"
  "CHANGELOG.md"
  "ROADMAP.md"
  "VERSION"
  "LICENSE"
  "docs"
)

ARCHIVE_PATHS=()
INCLUDED_REQUIRED=()
INCLUDED_OPTIONAL=()
SKIPPED_OPTIONAL=()

fail() {
  echo "ERROR: $*" >&2
  exit 2
}

timestamp() { date "+%Y-%m-%d %H:%M:%S"; }

elapsed() {
  local end
  end="$(date +%s)"
  echo "$((end - JOB_START))s"
}

begin_step() {
  STEP_START="$(date +%s)"
  echo
  echo "[$(timestamp)] ==> $1"
}

end_step() {
  local step_end elapsed_step
  step_end="$(date +%s)"
  elapsed_step="$((step_end - STEP_START))"
  echo "[$(timestamp)] <== Completed (${elapsed_step}s)"
}

join_lines() {
  local item
  if [ "$#" -eq 0 ]; then
    printf '%s\n' "None"
    return
  fi
  for item in "$@"; do
    printf '%s\n' "- $item"
  done
}

[ -d "$BASE_DIR" ] || fail "ACE server root does not exist: $BASE_DIR"

# Validate every required path before creating a timestamped backup directory so
# failed preflight does not leave an apparently valid empty backup behind.
cd "$BASE_DIR"
begin_step "Validating backup paths"
for path in "${REQUIRED_PATHS[@]}"; do
  if [ ! -e "$BASE_DIR/$path" ]; then
    fail "Required backup path missing: $path"
  fi
  ARCHIVE_PATHS+=("$path")
  INCLUDED_REQUIRED+=("$path")
  echo "Required: $path"
done

for path in "${OPTIONAL_PATHS[@]}"; do
  if [ -e "$BASE_DIR/$path" ]; then
    ARCHIVE_PATHS+=("$path")
    INCLUDED_OPTIONAL+=("$path")
    echo "Optional included: $path"
  else
    SKIPPED_OPTIONAL+=("$path")
    echo "WARNING: Optional backup path skipped: $path"
  fi
done
end_step

mkdir -p "$BACKUP_DIR"

echo "========================================================="
echo "ACE Infrastructure Backup"
echo "========================================================="
echo "Started : $(timestamp)"
echo "Host    : $(hostname)"
echo "Target  : $BACKUP_DIR"
echo "========================================================="

begin_step "Dumping ACE databases"
docker exec ace-db sh -c 'exec mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --no-tablespaces --databases ace_auth ace_shard ace_world' \
  | gzip > "$BACKUP_DIR/ace_databases.sql.gz"
end_step

begin_step "Backing up runtime and infrastructure files"
tar -czf "$BACKUP_DIR/ace_infrastructure.tar.gz" \
  -C "$BASE_DIR" \
  "${ARCHIVE_PATHS[@]}"
end_step

begin_step "Writing manifest"
{
  echo "Backup Created: $(timestamp)"
  echo "Host: $(hostname)"
  echo "Backup Type: ACE runtime + infrastructure"
  echo "Databases: ace_auth ace_shard ace_world"
  echo "Includes DAT files: no"
  echo "Includes permanent ACEMD data root: yes (data/)"
  echo "Backup Directory: $BACKUP_DIR"
  echo
  echo "Required paths included:"
  join_lines "${INCLUDED_REQUIRED[@]}"
  echo
  echo "Optional paths included:"
  join_lines "${INCLUDED_OPTIONAL[@]}"
  echo
  echo "Optional paths skipped:"
  join_lines "${SKIPPED_OPTIONAL[@]}"
} > "$BACKUP_DIR/manifest.txt"
end_step

begin_step "Verifying backup files"
gzip -t "$BACKUP_DIR/ace_databases.sql.gz"
tar -tzf "$BACKUP_DIR/ace_infrastructure.tar.gz" >/dev/null
end_step

echo
echo "========================================================="
echo "Backup Complete"
echo "========================================================="
echo "Finished: $(timestamp)"
echo "Elapsed : $(elapsed)"
echo "Status  : SUCCESS"
if [ "${#SKIPPED_OPTIONAL[@]}" -gt 0 ]; then
  echo "Warnings: ${#SKIPPED_OPTIONAL[@]} optional path(s) were skipped."
fi
echo
du -sh "$BACKUP_DIR"
ls -lh "$BACKUP_DIR"
