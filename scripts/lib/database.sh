#!/usr/bin/env bash
database_command() {
    case "${1:-status}" in
        status) compose ps "$ACE_DB_SERVICE" ;;
        logs) docker_logs db "${2:-150}" ;;
        shell) docker_shell db ;;
        restart) docker_restart db ;;
        *) die "Unknown database command: $1" ;;
    esac
}
