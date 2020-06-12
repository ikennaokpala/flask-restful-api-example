#!/bin/bash

set -e
set -x

python -m venv env-packages
source ./env-packages/bin/activate; \
pip install -r requirements.txt
python manage.py run

