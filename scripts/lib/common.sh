#!/usr/bin/env bash

info() { printf '[INFO] %s
' "$*"; }
warn() { printf '[WARN] %s
' "$*" >&2; }
die() { printf '[ERROR] %s
' "$*" >&2; exit 1; }

run_cmd() {
    if [[ "${ACE_DRY_RUN:-0}" == "1" ]]; then
        printf 'DRY RUN: no changes will be made
'
        printf 'Would execute:'
        printf ' %q' "$@"
        printf '
'
    else
        "$@"
    fi
}

compose_flavor() {
    if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
        printf 'docker-compose-plugin
'
        return 0
    fi
    if command -v docker-compose >/dev/null 2>&1 && docker-compose version >/dev/null 2>&1; then
        printf 'docker-compose-standalone
'
        return 0
    fi
    return 1
}

compose() {
    local flavor
    if ! flavor="$(compose_flavor)"; then
        die "Docker Compose is unavailable inside this environment. Rebuild the dashboard image with docker-compose-plugin, or install/provide docker-compose."
    fi

    local cmd=()
    case "$flavor" in
        docker-compose-plugin) cmd=(docker compose) ;;
        docker-compose-standalone) cmd=(docker-compose) ;;
        *) die "Unsupported Docker Compose provider: $flavor" ;;
    esac

    if [[ -f "$COMPOSE_FILE" ]]; then
        run_cmd "${cmd[@]}" -f "$COMPOSE_FILE" "$@"
    else
        run_cmd "${cmd[@]}" "$@"
    fi
}

service_alias() {
    case "${1:-all}" in
        dashboard|dash|ace-dashboard) printf 'dashboard
' ;;
        server|srv|ace|ace-server) printf 'server
' ;;
        db|database|mysql|ace-db|acedb) printf 'db
' ;;
        all|'') printf 'all
' ;;
        *) die "Unknown service alias: $1" ;;
    esac
}

service_name() {
    case "$(service_alias "${1:-all}")" in
        dashboard) printf '%s
' "$ACE_DASHBOARD_SERVICE" ;;
        server) printf '%s
' "$ACE_SERVER_SERVICE" ;;
        db) printf '%s
' "$ACE_DB_SERVICE" ;;
        all) printf 'all
' ;;
    esac
}

command_alias() {
    case "${1:-}" in
        log) printf 'logs
' ;;
        logs) printf 'logs
' ;;
        reboot) printf 'restart
' ;;
        restart) printf 'restart
' ;;
        database) printf 'db
' ;;
        mysql) printf 'db
' ;;
        dash) printf 'dashboard
' ;;
        srv|ace) printf 'server
' ;;
        *) printf '%s
' "${1:-}" ;;
    esac
}

service_command() {
    local svc="$(service_alias "${1:-server}")"
    local cmd="$(command_alias "${2:-status}")"
    shift 2 || true

    case "$cmd" in
        status)
            case "$svc" in
                dashboard) compose ps "$ACE_DASHBOARD_SERVICE" ;;
                server) compose ps "$ACE_SERVER_SERVICE" ;;
                db) compose ps "$ACE_DB_SERVICE" ;;
                all) docker_status ;;
            esac
            ;;
        logs) docker_logs "$svc" "${1:-150}" ;;
        shell) docker_shell "$svc" ;;
        restart) docker_restart "$svc" ;;
        rebuild)
            [[ "$svc" == "server" || "$svc" == "db" ]] && warn "Rebuilding $svc is not normally required unless its image or build context changed."
            docker_rebuild "$svc"
            ;;
        *) die "Unknown command '$cmd' for service '$svc'. Run ./manage.sh help." ;;
    esac
}

ace_version() {
    echo "ACE Management Utility: $ACE_MANAGE_VERSION"
    if [[ -f "$ACE_ROOT/dashboard/VERSION" ]]; then
        echo "ACE Management Dashboard: $(cat "$ACE_ROOT/dashboard/VERSION")"
    fi
    if [[ -f "$ACE_ROOT/dashboard/PROJECT.md" ]]; then
        grep -E '^(version|phase|milestone|status|build):' "$ACE_ROOT/dashboard/PROJECT.md" || true
    fi
}
