SHELL = /bin/bash
SUDO := $(shell which sudo)
PYENV_ROOT = $(HOME)/.pyenv
PYTHONDONTWRITEBYTECODE = 1
PIPENV_IGNORE_VIRTUALENVS = 1
VENV_HOME_DIR = '\$\(pipenv --venv)'
LSARP_API_PYTHON_BIN_PATH = /usr/local/bin
PATH := $(PYENV_ROOT)/shims:$(PYENV_ROOT)/bin:$(PATH)
LSARP_API_PYTHON_INSTALL_VERSION := 3.8.5
LSARP_API_PYTHON_VERSION := $(shell v=$(LSARP_API_PYTHON_INSTALL_VERSION); echo $${v:0:3})
LSARP_API_PYTHON_MAIN_VERSION := $(shell v=$(LSARP_API_PYTHON_INSTALL_VERSION); echo $${v:0:1})

args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

%:
	@:

include app/builds/makers/common.mk
include app/builds/makers/db.mk
include app/builds/makers/development.mk
include app/builds/makers/production.mk
include app/builds/makers/python.mk
include app/builds/makers/system.mk
include app/builds/makers/tests.mk
