.PHONY: build-yum-packages  build-apt-packages build-homebrew-packages

build-yum-packages:
	$(SUDO) yum update -y
	$(SUDO) yum groupinstall 'Development Tools' -y 
	$(SUDO) yum install -y sqlite-devel readline-devel curl which wget make openssl-devel bzip2-devel xz-devel libffi-devel zlib-devel python$(LSARP_API_PYTHON_MAIN_VERSION)-devel libevent-devel postgresql-devel -y

build-apt-packages:
	$(SUDO) apt-get update -y
	$(SUDO) apt-get install -y libbz2-dev libsqlite3-dev libreadline6-dev libffi-dev python3-dev libjpeg-dev libjpeg8-dev python3-pip python3-psycopg2 git curl wget libssl-dev build-essential liblzma-dev make zlib1g-dev python$(LSARP_API_PYTHON_MAIN_VERSION)-dev libevent-dev libblas-dev libatlas-base-dev python$(LSARP_API_PYTHON_MAIN_VERSION)-venv libpq-dev postgresql-contrib -y --no-install-recommends
	$(SUDO) apt-get clean

build-homebrew-packages:
	# Sudo is not required as running Homebrew as root is extremely dangerous and no longer supported as Homebrew does not drop privileges on installation you would be giving all build scripts full access to your system
	# Fails if any of the packages are already installed, ignore and continue - if it's a problem the latest build steps will fail with missing headers
	brew update

	brew install terraform ansible
