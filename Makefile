SHELL = /bin/bash
PYTHON_VERSION = 3.8
PYTHON_MAIN_VERSION = 3
PYTHON_INSTALL_VERSION = 3.8.5
PYTHON_BIN_PATH = /usr/local/bin

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
	yum install sudo -y
	$(SUDO) yum update -y
	$(SUDO) yum groupinstall 'Development Tools' -y 
	$(SUDO) yum install -y curl which wget make openssl-devel bzip2-devel xz-devel libffi-devel zlib-devel python$(PYTHON_MAIN_VERSION)-devel libevent-devel postgresql-devel -y
	$(SUDO) wget https://www.python.org/ftp/python/$(PYTHON_INSTALL_VERSION)/Python-$(PYTHON_INSTALL_VERSION).tgz && tar xvf Python-$(PYTHON_INSTALL_VERSION).tgz && cd Python-$(PYTHON_INSTALL_VERSION)/ && ./configure --enable-optimizations && make altinstall && cd .. && rm -rf Python-$(PYTHON_INSTALL_VERSION)/
	$(SUDO) curl --silent https://bootstrap.pypa.io/get-pip.py | python$(PYTHON_VERSION)
	$(SUDO) rm -fr $(PYTHON_BIN_PATH)/python$(PYTHON_MAIN_VERSION) && ln $(PYTHON_BIN_PATH)/python$(PYTHON_VERSION) $(PYTHON_BIN_PATH)/python$(PYTHON_MAIN_VERSION)
	pip3 install --upgrade --no-cache-dir pipenv

.PHONY: apk-packages
apk-packages:
	apt-get install sudo -y
	$(SUDO) apk update -y
	$(SUDO) apk install -y python-pip curl wget build-essential liblzma-dev make zlib1g-dev python$(PYTHON_MAIN_VERSION)-dev libevent-dev libblas-dev libatlas-base-dev python$(PYTHON_MAIN_VERSION)-venv pipenv python-psycopg2 libpq-dev -y
	$(SUDO) apk clean
	$(SUDO) wget https://www.python.org/ftp/python/$(PYTHON_INSTALL_VERSION)/Python-$(PYTHON_INSTALL_VERSION).tgz && tar xvf Python-$(PYTHON_INSTALL_VERSION).tgz && cd Python-$(PYTHON_INSTALL_VERSION)/ && ./configure --enable-optimizations --with-zlib && make altinstall && cd .. && rm -rf Python-$(PYTHON_INSTALL_VERSION)/
	$(SUDO) curl --silent https://bootstrap.pypa.io/get-pip.py | python$(PYTHON_VERSION)
	$(SUDO) rm -fr $(PYTHON_BIN_PATH)/python$(PYTHON_MAIN_VERSION) && ln $(PYTHON_BIN_PATH)/python$(PYTHON_VERSION) $(PYTHON_BIN_PATH)/python$(PYTHON_MAIN_VERSION)
	pip3 install --upgrade --no-cache-dir pipenv

.PHONY: apt-packages
apt-packages:
	apt-get install sudo -y --no-install-recommends
	$(SUDO) apt-get update -y
	$(SUDO) apt-get install -y python-pip curl wget build-essential liblzma-dev make zlib1g-dev python$(PYTHON_MAIN_VERSION)-dev libevent-dev libblas-dev libatlas-base-dev python$(PYTHON_MAIN_VERSION)-venv python-psycopg2 libpq-dev -y --no-install-recommends
	$(SUDO) apt-get clean
	$(SUDO) wget https://www.python.org/ftp/python/$(PYTHON_INSTALL_VERSION)/Python-$(PYTHON_INSTALL_VERSION).tgz && tar xvf Python-$(PYTHON_INSTALL_VERSION).tgz && cd Python-$(PYTHON_INSTALL_VERSION)/ && ./configure --enable-optimizations --with-zlib && make altinstall && cd .. && rm -rf Python-$(PYTHON_INSTALL_VERSION)/
	$(SUDO) curl --silent https://bootstrap.pypa.io/get-pip.py | python$(PYTHON_VERSION)
	$(SUDO) rm -fr $(PYTHON_BIN_PATH)/python$(PYTHON_MAIN_VERSION) && ln $(PYTHON_BIN_PATH)/python$(PYTHON_VERSION) $(PYTHON_BIN_PATH)/python$(PYTHON_MAIN_VERSION)
	pip3 install --upgrade --no-cache-dir pipenv

.PHONY: homebrew-packages
homebrew-packages:
	# Sudo is not required as running Homebrew as root is extremely dangerous and no longer supported as Homebrew does not drop privileges on installation you would be giving all build scripts full access to your system
	# Fails if any of the packages are already installed, ignore and continue - if it's a problem the latest build steps will fail with missing headers
	brew update
	brew install python pipenv
	$(SUDO) easy_install pip
	python$(PYTHON_VERSION) -m pip install --upgrade pip pipenv

.PHONY: clean python-packages install tests run all

clean:
	pipenv clean
	pipenv --rm
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

python-packages:
	pipenv sync --dev

install: system-packages python-packages

tests:
	FLASK_ENV=test pipenv run db_create
	FLASK_ENV=test pipenv run tests
	FLASK_ENV=test pipenv run db_drop

test:
	FLASK_ENV=test pipenv run db_create
	FLASK_ENV=test pipenv run test $(call args, app/tests/test*.py)
	FLASK_ENV=test pipenv run db_drop

format:
	pipenv run format

run:
	FLASK_ENV=production pipenv run start

dev:
	FLASK_ENV=development pipenv run start

console:
	pipenv run console

dev_console:
	FLASK_ENV=development pipenv run console

db_init:
	pipenv run db_init

db_create:
	pipenv run db_create

db_seed:
	pipenv run db_seed

db_drop:
	pipenv run db_drop

db_migration:
	pipenv run db_migration

db_migrate:
	pipenv run db_migrate

all: clean install tests run
