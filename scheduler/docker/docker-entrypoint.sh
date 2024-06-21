#!/bin/bash
set -euo pipefail
#!/bin/bash
set -e

if [[ "$1" =~ "scheduler" ]]; then
    python main.py
fi

if [[ "$1" =~ "shell" ]]; then
    /bin/bash
fi

exec "$@"

