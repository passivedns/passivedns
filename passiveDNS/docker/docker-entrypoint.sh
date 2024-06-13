#!/bin/bash
set -euo pipefail

if [[ "$1" = 'webserver' ]]; then
    python main.py
elif [[ "$1" = 'create-user' ]]; then
    python ctl/cli.py create-user "${@:2}"
elif [[ "$1" = 'reset-password' ]]; then
    python ctl/cli.py reset-password "${@:2}"
elif [[ "$1" = 'delete-user' ]]; then
    python ctl/cli.py delete-user "${@:2}"
else
    exec "$@"
fi