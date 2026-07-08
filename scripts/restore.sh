#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/opt/acserver"
BACKUP_DIR="${1:-}"
JOB_START="$(date +%s)"

timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

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

if [ -z "$BACKUP_DIR" ]; then
  echo "Usage: scripts/restore.sh backups/runtime/YYYY-MM-DD_HH-MM-SS"
  exit 1
fi

if [ ! -d "$BACKUP_DIR" ]; then
  echo "Backup directory not found: $BACKUP_DIR"
  exit 1
fi

DB_BACKUP="$BACKUP_DIR/ace_databases.sql.gz"
INFRA_BACKUP="$BACKUP_DIR/ace_infrastructure.tar.gz"

if [ ! -f "$DB_BACKUP" ]; then
  echo "Missing database backup: $DB_BACKUP"
  exit 1
fi

if [ ! -f "$INFRA_BACKUP" ]; then
  echo "Missing infrastructure backup: $INFRA_BACKUP"
  exit 1
fi

cd "$BASE_DIR"

echo "========================================================="
echo "ACE Infrastructure Restore"
echo "========================================================="
echo "Started : $(timestamp)"
echo "Host    : $(hostname)"
echo "Source  : $BACKUP_DIR"
echo "========================================================="
echo
echo "This will restore:"
echo "  - ace_auth"
echo "  - ace_shard"
echo "  - ace_world"
echo "  - infrastructure/config files"
echo
read -r -p "Continue? Type RESTORE to proceed: " CONFIRM

if [ "$CONFIRM" != "RESTORE" ]; then
  echo "Restore cancelled."
  exit 1
fi

begin_step "Creating pre-restore safety backup"
scripts/backup.sh
end_step

begin_step "Stopping ACE server container"
docker compose stop ace-server
end_step

begin_step "Restoring ACE databases"
gunzip -c "$DB_BACKUP" | docker exec -i ace-db sh -c 'exec mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD"'
end_step

begin_step "Restoring infrastructure/config files"
tar -xzf "$INFRA_BACKUP" -C "$BASE_DIR"
end_step

begin_step "Restarting ACE stack"
docker compose up -d
end_step

begin_step "Verifying containers"
docker compose ps
end_step

echo
echo "========================================================="
echo "Restore Complete"
echo "========================================================="
echo "Finished: $(timestamp)"
echo "Elapsed : $(elapsed)"
echo "Status  : SUCCESS"
echo "========================================================="
