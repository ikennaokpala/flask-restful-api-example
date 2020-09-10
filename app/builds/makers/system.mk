.PHONY: build-system build build-ubuntu build-centos build-darwin

build-system:
	if [ -x /usr/bin/apt-get ]; then $(MAKE) build-ubuntu; fi
	if [ -x /usr/bin/yum ];     then $(MAKE) build-centos; fi
	if [ -x /usr/local/bin/brew -a `uname` = Darwin ]; then $(MAKE) build-darwin; fi

build-ubuntu: build-apt-packages pyenv-packages sync-packages

build-centos: build-yum-packages pyenv-packages sync-packages

build-darwin: build-homebrew-packages build-homebrew-python-packages sync-packages

build: docker-build
install: build-system
publish: docker-publish
