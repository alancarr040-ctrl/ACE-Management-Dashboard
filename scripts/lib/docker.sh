#!/usr/bin/env bash

docker_status() { compose ps; }
docker_start() { compose up -d; }
docker_stop() { compose stop; }

docker_restart() {
    local svc; svc="$(service_name "${1:-all}")"
    if [[ "$svc" == "all" ]]; then
        compose restart
    else
        compose restart "$svc"
    fi
}

docker_rebuild() {
    local svc; svc="$(service_name "${1:-all}")"
    if [[ "$svc" == "all" ]]; then
        compose up -d --build
    else
        compose up -d --build "$svc"
    fi
}

docker_logs() {
    local svc lines
    svc="$(service_name "${1:-server}")"
    lines="${2:-150}"
    [[ "$svc" != "all" ]] || die "Logs require a single service alias."
    compose logs --tail "$lines" "$svc"
}

docker_shell() {
    local svc
    svc="$(service_name "${1:-server}")"
    [[ "$svc" != "all" ]] || die "Shell requires a single service alias."
    compose exec "$svc" /bin/sh
}
