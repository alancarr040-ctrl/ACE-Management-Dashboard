#!/usr/bin/env bash
backup_command() {
    case "${1:-list}" in
        create)
            [[ -x "$ACE_ROOT/scripts/backup.sh" ]] || die "Backup script is not executable: $ACE_ROOT/scripts/backup.sh"
            if [[ "${ACE_DRY_RUN:-0}" == "1" ]]; then
                run_cmd "$ACE_ROOT/scripts/backup.sh"
            else
                "$ACE_ROOT/scripts/backup.sh"
            fi
            ;;
        list)
            if [[ -d "$ACE_ROOT/backups" ]]; then
                find "$ACE_ROOT/backups" -mindepth 1 -maxdepth 1 -type d -printf '%TY-%Tm-%Td %TH:%TM  %p\n' | sort -r
            else
                warn "No backups directory found at $ACE_ROOT/backups"
            fi
            ;;
        verify)
            if [[ -d "$ACE_ROOT/backups" ]]; then
                while IFS= read -r d; do
                    if [[ -f "$d/MANIFEST.txt" || -f "$d/manifest.txt" ]]; then
                        echo "VERIFIED $d"
                    else
                        echo "PARTIAL  $d (manifest missing)"
                    fi
                done < <(find "$ACE_ROOT/backups" -mindepth 1 -maxdepth 1 -type d | sort)
            else
                warn "No backups directory found at $ACE_ROOT/backups"
            fi
            ;;
        *) die "Unknown backup command: $1" ;;
    esac
}
