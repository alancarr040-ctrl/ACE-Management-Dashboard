#!/usr/bin/env bash
set -euo pipefail

ACE_MANAGE_VERSION="1.1.1"
ACE_ROOT="${ACE_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
COMPOSE_FILE="${COMPOSE_FILE:-$ACE_ROOT/docker-compose.yml}"
ACE_DASHBOARD_SERVICE="${ACE_DASHBOARD_SERVICE:-ace-dashboard}"
ACE_SERVER_SERVICE="${ACE_SERVER_SERVICE:-ace-server}"
ACE_DB_SERVICE="${ACE_DB_SERVICE:-ace-db}"
ACE_DRY_RUN=0

source "$ACE_ROOT/scripts/lib/common.sh"
source "$ACE_ROOT/scripts/lib/docker.sh"
source "$ACE_ROOT/scripts/lib/server.sh"
source "$ACE_ROOT/scripts/lib/dashboard.sh"
source "$ACE_ROOT/scripts/lib/database.sh"
source "$ACE_ROOT/scripts/lib/backup.sh"
source "$ACE_ROOT/scripts/lib/doctor.sh"

usage() {
cat <<USAGE
ACE Management Utility v$ACE_MANAGE_VERSION

Usage:
  ./manage.sh [--dry-run] <command>
  ./manage.sh [--dry-run] <category> <command> [options]
  ./manage.sh [--dry-run] <command> <service> [options]

System:
  status                 Show Docker Compose service status
  start                  Start the ACE stack
  stop                   Stop the ACE stack
  restart [service]      Restart all services or one service alias
  rebuild [service]      Rebuild all services or one service alias

Containers:
  dashboard logs|shell|restart|rebuild
  server logs|shell|restart
  db logs|shell|restart

Reversed forms are also supported:
  logs server 50
  restart server
  rebuild dashboard
  shell db

Backups:
  backup create          Run the existing runtime backup script
  backup list            List backup folders
  backup verify          Show backup folders and manifest status

Maintenance:
  doctor                 Run local environment checks
  health                 Alias for doctor

Information:
  version                Show utility and dashboard versions
  help                   Show this help

Options:
  --dry-run              Show what would run without changing anything

Service aliases:
  dashboard, dash
  server, srv, ace
  db, database, mysql
  all

Command aliases:
  logs, log
  restart, reboot
USAGE
}

parse_options() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dry-run|-n)
                ACE_DRY_RUN=1
                shift
                ;;
            --)
                shift
                break
                ;;
            *)
                break
                ;;
        esac
    done
    REMAINING_ARGS=("$@")
}

main() {
    local REMAINING_ARGS=()
    parse_options "$@"
    set -- "${REMAINING_ARGS[@]}"

    local category="${1:-help}"
    shift || true

    category="$(command_alias "$category")"

    # Accept reversed forms such as "restart server", "logs server", and "shell db".
    case "$category" in
        logs)
            docker_logs "${1:-server}" "${2:-150}"
            return
            ;;
        shell)
            docker_shell "${1:-server}"
            return
            ;;
        restart)
            docker_restart "${1:-all}"
            return
            ;;
        rebuild)
            docker_rebuild "${1:-all}"
            return
            ;;
    esac

    # Accept category-first forms such as "server logs" and "db shell".
    case "$category" in
        help|-h|--help) usage ;;
        version) ace_version ;;
        status) docker_status ;;
        start) docker_start ;;
        stop) docker_stop ;;
        dashboard|server|db|database|mysql|srv|ace|dash)
            local svc cmd
            svc="$(service_alias "$category")"
            cmd="$(command_alias "${1:-status}")"
            shift || true
            service_command "$svc" "$cmd" "$@"
            ;;
        backup|backups)
            local cmd
            cmd="$(command_alias "${1:-list}")"
            shift || true
            backup_command "$cmd" "$@"
            ;;
        doctor|health) doctor_run ;;
        *) die "Unknown command: $category. Run ./manage.sh help." ;;
    esac
}

main "$@"
