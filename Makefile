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

.PHONY: apk-packages
apk-packages:
	$(SUDO) apk update -y
	$(SUDO) apk install -y python-pip
	$(SUDO) pip install --user virtualenv
	python3 -m venv env-packages

.PHONY: apt-packages
apt-packages:
	$(SUDO) apt-get update -y
	$(SUDO) apt-get install -y python-pip
	$(SUDO) pip install --user virtualenv
	python3 -m venv env-packages

.PHONY: homebrew-packages
homebrew-packages:
	# Sudo is not required as running Homebrew as root is extremely dangerous and no longer supported as Homebrew does not drop privileges on installation you would be giving all build scripts full access to your system
	# Fails if any of the packages are already installed, ignore and continue - if it's a problem the latest build steps will fail with missing headers
	brew update
	brew install python
	sudo easy_install pip
	sudo pip install --user virtualenv
	python3 -m venv env-packages

.PHONY: clean python-packages install tests run all

clean:
	sudo rm -rf env-packages
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

python-packages:
	source ./env-packages/bin/activate; \
	sudo pip install -r requirements.txt

install: system-packages python-packages

tests:
	source ./env-packages/bin/activate; \
	python manage.py tests

run:
	source ./env-packages/bin/activate; \
	python manage.py run

all: clean install tests run
