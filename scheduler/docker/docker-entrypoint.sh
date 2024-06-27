#!/bin/bash
set -euo pipefail
#!/bin/bash
set -e

if [[ "$1" =~ "scheduler" ]]; then
    poetry run celery -A tasks worker --loglevel=info --purge -B -P threads
fi
if [[ "$1" =~ "shell" ]]; then
    /bin/bash
fi

exec "$@"

