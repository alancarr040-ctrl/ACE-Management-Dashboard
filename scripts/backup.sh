#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/opt/acserver"
BACKUP_ROOT="$BASE_DIR/backups/runtime"
STAMP="$(date +%Y-%m-%d_%H-%M-%S)"
BACKUP_DIR="$BACKUP_ROOT/$STAMP"
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

echo "========================================================="
echo "ACE Infrastructure Backup"
echo "========================================================="
echo "Started : $(timestamp)"
echo "Host    : $(hostname)"
echo "Target  : $BACKUP_DIR"
echo "========================================================="

cd "$BASE_DIR"
mkdir -p "$BACKUP_DIR"

begin_step "Dumping ACE databases"
docker exec ace-db sh -c 'exec mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --no-tablespaces --databases ace_auth ace_shard ace_world' \
  | gzip > "$BACKUP_DIR/ace_databases.sql.gz"
end_step

begin_step "Backing up infrastructure/config files"
tar -czf "$BACKUP_DIR/ace_infrastructure.tar.gz" \
  .env \
  docker-compose.yml \
  PROJECT.md \
  README.md \
  VERSION \
  scripts \
  docs \
  ace/Config \
  ace/Content \
  ace/Mods
end_step

begin_step "Writing manifest"
cat > "$BACKUP_DIR/manifest.txt" <<EOF
Backup Created: $(timestamp)
Host: $(hostname)
Backup Type: ACE runtime + infrastructure
Databases: ace_auth ace_shard ace_world
Includes DAT files: no
Backup Directory: $BACKUP_DIR
EOF
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
echo
du -sh "$BACKUP_DIR"
ls -lh "$BACKUP_DIR"
