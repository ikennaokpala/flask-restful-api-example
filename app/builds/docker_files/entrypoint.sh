#!/bin/bash

set -e
set -x

source $(pipenv --venv)/bin/activate

if [ ${FLASK_ENV} == "production" ]; then
  pipenv sync
  make start
else
  pipenv sync --dev
  make server
fi
