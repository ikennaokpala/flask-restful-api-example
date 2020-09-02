#!/bin/bash

set -e
set -x

source $(pipenv --venv)/bin/activate

if [ ${FLASK_ENV} == "production" ]; then
  pipenv sync
  make run
else
  pipenv sync --dev
  make dev
fi
