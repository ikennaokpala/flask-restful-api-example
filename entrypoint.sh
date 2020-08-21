#!/bin/bash

set -e
set -x

source $(pipenv --venv)/bin/activate

if [ ${FLASK_ENV} == "development" ]; then
  pipenv sync --dev
  make dev
else
  pipenv sync
  make run
fi
