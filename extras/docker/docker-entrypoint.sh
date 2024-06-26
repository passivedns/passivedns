#!/bin/bash
set -euo pipefail

if [[ "$1" = 'webserver' ]]; then
    poetry run uvicorn passiveDNS.webserver:app --host 0.0.0.0 --port 8080
elif [[ "$1" = 'create-user' ]]; then
    poetry run python passiveDNS/ctl/cli.py create-user "${@:2}"
elif [[ "$1" = 'reset-password' ]]; then
    python ctl/cli.py reset-password "${@:2}"
elif [[ "$1" = 'delete-user' ]]; then
    python ctl/cli.py delete-user "${@:2}"
elif [[ "$1" = 'scheduler' ]]; then
    poetry run celery -A passiveDNS.scheduler.tasks worker --loglevel=info
else
    exec "$@"
fi
