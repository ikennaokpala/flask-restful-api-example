# Environment variables
SHELL = /bin/bash
GITHUB_USERNAME ?= wgbot
SUDO := $(shell which sudo)
PYENV_ROOT ?= $(HOME)/.pyenv
PYTHONDONTWRITEBYTECODE ?= 1
LSARP_API_IMAGE_TAG ?= latest
LSARP_GITHUB_ORG_NAME ?= lsarp
PIPENV_IGNORE_VIRTUALENVS ?= 1
LSARP_API_OS_PLATFORM ?= centos
LSARP_API_GITHUB_REPO_NAME ?= api
LSARP_API_OS_PLATFORMS = centos ubuntu
LSARP_API_VERSION ?= $(shell cat VERSION)
LSARP_API_PYTHON_BIN_PATH ?= /usr/local/bin
DOCKER_IMAGES_DOMAIN ?= docker.pkg.github.com
PATH := $(PYENV_ROOT)/shims:$(PYENV_ROOT)/bin:$(PATH)
LSARP_API_PYTHON_INSTALL_VERSION ?= $(shell cat .python-version)
LSARP_API_IMAGE_NAME ?= ${LSARP_API_OS_PLATFORM}:${LSARP_API_IMAGE_TAG}
LSARP_API_DOCKER_VERSION ?= $(shell cat src/builds/docker_files/VERSION)
LSARP_API_DOCKER_VERSIONS ?= $(LSARP_API_DOCKER_VERSION) $(LSARP_API_IMAGE_TAG)
LSARP_API_PYTHON_VERSION := $(shell v=$(LSARP_API_PYTHON_INSTALL_VERSION); echo $${v:0:3})
LSARP_API_PYTHON_MAIN_VERSION := $(shell v=$(LSARP_API_PYTHON_INSTALL_VERSION); echo $${v:0:1})
LSARP_API_GITHUB_REPOSITORY ?= $(shell git remote get-url origin | sed 's/.*\/\(.*\)\/\(.*\)\.git/\1\/\2/')
LSARP_API_DOCKER_ENDPOINT ?= $(DOCKER_IMAGES_DOMAIN)/$(LSARP_GITHUB_ORG_NAME)/$(LSARP_API_GITHUB_REPO_NAME)

# Variables
args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

# Modules
include src/builds/makers/db.mk
include src/builds/makers/tests.mk
include src/builds/makers/common.mk
include src/builds/makers/docker.mk
include src/builds/makers/python.mk
include src/builds/makers/system.mk
include src/builds/makers/production.mk
include src/builds/makers/development.mk

# Match any (command/task) pattern rule https://www.gnu.org/software/make/manual/make.html#Match_002dAnything-Rules
%:
	@:
