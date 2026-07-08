#!/usr/bin/env bash

doctor_run() {
    local failures=0
    command -v docker >/dev/null 2>&1 && echo "OK docker command found" || { echo "FAIL docker command missing"; failures=$((failures+1)); }

    if flavor="$(compose_flavor)"; then
        echo "OK docker compose available ($flavor)"
    else
        echo "FAIL docker compose unavailable"
        failures=$((failures+1))
    fi

    [[ -f "$COMPOSE_FILE" ]] && echo "OK compose file found: $COMPOSE_FILE" || { echo "FAIL compose file missing: $COMPOSE_FILE"; failures=$((failures+1)); }
    [[ -S /var/run/docker.sock ]] && echo "OK docker socket mounted" || echo "WARN docker socket not detected at /var/run/docker.sock"
    [[ -f "$ACE_ROOT/dashboard/PROJECT.md" ]] && echo "OK project metadata found" || { echo "WARN project metadata missing"; }
    [[ -x "$ACE_ROOT/manage.sh" ]] && echo "OK manage.sh executable" || { echo "FAIL manage.sh is not executable"; failures=$((failures+1)); }
    if [[ "$failures" -gt 0 ]]; then
        return 1
    fi
    echo "OK doctor checks passed"
}
