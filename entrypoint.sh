#!/bin/bash

set -e
set -x

source $(pipenv --venv)/bin/activate

if [ ${FLASK_ENV} == "development" ]; then
  pipenv sync --dev
  pipenv run dev
else
  pipenv sync
  FLASK_ENV=production pipenv run prod
fi
