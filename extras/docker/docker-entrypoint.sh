#!/bin/bash
set -euo pipefail

if [[ "$1" = 'webserver' ]]; then
    poetry run uvicorn webserver:app --host 0.0.0.0
elif [[ "$1" = 'create-user' ]]; then
    poetry run python PassiveDNS/ctl/cli.py create-user "${@:2}"
elif [[ "$1" = 'reset-password' ]]; then
    python ctl/cli.py reset-password "${@:2}"
elif [[ "$1" = 'delete-user' ]]; then
    python ctl/cli.py delete-user "${@:2}"
else
    exec "$@"
fi
