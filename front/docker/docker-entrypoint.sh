#!/bin/bash
set -e

if [[ "$1" =~ "dev" ]]; then
    if [[ ! -f ".node_installed" ]]; then
      echo ".node_installed not found, installing node modules"
      rm -rf node_modules
      npm install
      touch .node_installed
    fi
    npm run serve
fi

if [[ "$1" =~ "shell" ]]; then
    /bin/bash
fi

exec "$@"