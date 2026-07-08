#!/usr/bin/env bash
dashboard_command() {
    case "${1:-status}" in
        status) compose ps "$ACE_DASHBOARD_SERVICE" ;;
        logs) docker_logs dashboard "${2:-150}" ;;
        shell) docker_shell dashboard ;;
        restart) docker_restart dashboard ;;
        rebuild) docker_rebuild dashboard ;;
        *) die "Unknown dashboard command: $1" ;;
    esac
}
