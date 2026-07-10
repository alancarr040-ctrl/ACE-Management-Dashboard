# 3.1.2.1 Known Issues and Deferred Work

## Compatibility state paths

Automation and Notifications continue to store current writable state beneath:

```text
/opt/acserver/backups/runtime/
```

The ownership preparation script manages this location so the dashboard can operate safely under the deployment account. Moving these services beneath `/opt/acserver/data/` is intentionally deferred to a future storage-registry package.

## Script executable permissions

Windows ZIP extraction followed by FTP or SCP upload may remove Unix executable permissions from shell scripts. Deployment documentation therefore uses:

```bash
sudo bash ./scripts/prepare-dashboard-owner.sh /opt/acserver
```

This is a packaging-platform compatibility issue, not a script execution failure.

## Trailing slash display

Passing `/opt/acserver/` with a trailing slash may produce cosmetic double slashes in preparation-script status output, such as `/opt/acserver//data`. Linux path handling is unaffected. Input normalization is deferred as non-blocking polish.

## Future storage registry

Writable storage paths are still known by deployment scripts individually. A future package should introduce one central storage registry used by preparation, health checks, backup, and subsystem initialization.

## Backup file modes

New backup artifacts may initially be created with mode `0644` and are normalized by owner preparation when rerun. A future backup polish change may set a stricter creation umask directly in the backup process.
