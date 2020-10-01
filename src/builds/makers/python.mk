.PHONY: pyenv-packages build-homebrew-python-packages sync-packages

build-homebrew-python-packages:
	brew install pyenv pipenv
	pyenv install $(LSARP_API_PYTHON_INSTALL_VERSION)
	pyenv local $(LSARP_API_PYTHON_INSTALL_VERSION)
	python$(LSARP_API_PYTHON_VERSION) -m pip install --upgrade pip pipenv

pyenv-packages:
	@if [[ ! -d $(PYENV_ROOT) ]] ; then sudo -u `whoami` curl https://pyenv.run | bash; fi	
	pyenv update
	pyenv install $(LSARP_API_PYTHON_INSTALL_VERSION)
	pyenv local $(LSARP_API_PYTHON_INSTALL_VERSION)
	pyenv global $(LSARP_API_PYTHON_INSTALL_VERSION)
	$(SUDO) rm -fr $(LSARP_API_PYTHON_BIN_PATH)/python && $(SUDO) ln $(PYENV_ROOT)/versions/$(LSARP_API_PYTHON_INSTALL_VERSION)/bin/python$(LSARP_API_PYTHON_MAIN_VERSION) $(LSARP_API_PYTHON_BIN_PATH)/python
	$(SUDO) rm -fr $(LSARP_API_PYTHON_BIN_PATH)/pip && $(SUDO) ln $(PYENV_ROOT)/versions/$(LSARP_API_PYTHON_INSTALL_VERSION)/bin/pip$(LSARP_API_PYTHON_MAIN_VERSION) $(LSARP_API_PYTHON_BIN_PATH)/pip
	$(PYENV_ROOT)/versions/$(LSARP_API_PYTHON_INSTALL_VERSION)/bin/pip$(LSARP_API_PYTHON_MAIN_VERSION) install --upgrade --no-cache-dir pip
	$(PYENV_ROOT)/versions/$(LSARP_API_PYTHON_INSTALL_VERSION)/bin/pip$(LSARP_API_PYTHON_MAIN_VERSION) install pipenv
	$(SUDO) ln $(PYENV_ROOT)/versions/$(LSARP_API_PYTHON_INSTALL_VERSION)/bin/pipenv $(LSARP_API_PYTHON_BIN_PATH)/pipenv
	echo 'export PYENV_ROOT="${PYENV_ROOT}"' >> ~/.bashrc
	echo 'export PATH="${PYENV_ROOT}/bin:${PATH}"' >> ~/.bashrc
	echo 'eval "$(pyenv init -)"' >> ~/.bashrc

sync-packages:
	@if [ -x /usr/bin/apt-get ]; then sudo pipenv sync --dev; fi
	@if [ -x /usr/bin/yum ];     then pipenv sync --dev; fi
	@if [ -x /usr/local/bin/brew -a `uname` = Darwin ]; then pipenv sync --dev; fi
