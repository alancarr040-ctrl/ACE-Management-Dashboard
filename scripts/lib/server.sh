#!/usr/bin/env bash
server_command() {
    case "${1:-status}" in
        status) compose ps "$ACE_SERVER_SERVICE" ;;
        logs) docker_logs server "${2:-150}" ;;
        shell) docker_shell server ;;
        restart) docker_restart server ;;
        *) die "Unknown server command: $1" ;;
    esac
}
