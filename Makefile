SHELL=/bin/bash

SUDO := $(shell which sudo)

args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

%:
	@:

.PHONY: system-packages
system-packages:
	if [ -x /sbin/apk ];        then $(MAKE) apk-packages; fi
	if [ -x /usr/bin/apt-get ]; then $(MAKE) apt-packages; fi
	if [ -x /usr/bin/yum ];     then $(MAKE) yum-packages; fi
	if [ -x /usr/local/bin/brew -a `uname` = Darwin ]; then $(MAKE) homebrew-packages; fi

.PHONY: yum-packages
yum-packages:
	$(SUDO) yum update -y
	$(SUDO) yum install -y python-pip
	$(SUDO) pip install --user virtualenv
	python3 -m venv env-packages
	source ./env-packages/bin/activate; \
	pip install --upgrade pip

.PHONY: apk-packages
apk-packages:
	$(SUDO) apk update -y
	$(SUDO) apk install -y python-pip
	$(SUDO) pip install --user virtualenv
	python3 -m venv env-packages
	source ./env-packages/bin/activate; \
	pip install --upgrade pip

.PHONY: apt-packages
apt-packages:
	$(SUDO) apt-get update -y
	$(SUDO) apt-get install python3-venv -y
	$(SUDO) apt-get install -y python-pip
	$(SUDO) pip install --user virtualenv
	python3 -m venv env-packages
	source ./env-packages/bin/activate; \
	pip install --upgrade pip

.PHONY: homebrew-packages
homebrew-packages:
	# Sudo is not required as running Homebrew as root is extremely dangerous and no longer supported as Homebrew does not drop privileges on installation you would be giving all build scripts full access to your system
	# Fails if any of the packages are already installed, ignore and continue - if it's a problem the latest build steps will fail with missing headers
	brew update
	brew install python
	$(SUDO) easy_install pip
	$(SUDO) pip install --user virtualenv
	python3 -m venv env-packages
	source ./env-packages/bin/activate; \
	pip install --upgrade pip

.PHONY: clean python-packages install tests run all

clean:
	$(SUDO) rm -rf env-packages
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

python-packages:
	source ./env-packages/bin/activate; \
	pip install -r requirements.txt

install: system-packages python-packages

createdb:
	source ./env-packages/bin/activate; \
	python manage.py createdb $(call args, development)

dropdb:
	source ./env-packages/bin/activate; \
	python manage.py dropdb $(call args, development)

tests:
	source ./env-packages/bin/activate; \
	python manage.py tests

test:
	source ./env-packages/bin/activate; \
	python manage.py test $(call args, test*.py)

run:
	source ./env-packages/bin/activate; \
	python manage.py run

db_init:
	source ./env-packages/bin/activate; \
	python manage.py db init

all: clean install tests run
