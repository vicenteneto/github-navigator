#!/bin/bash

function go_to_source_directory {
    # Gets the current directory for the service configuration.
    SCRIPTS_DIRECTORY="$(dirname "${BASH_SOURCE[0]}")"
    HOME_DIRECTORY=`cd ${SCRIPTS_DIRECTORY} && pwd`

    echo "INFO: Changing current directory to \"${HOME_DIRECTORY}\"."
    cd ${HOME_DIRECTORY}
}

function found_python_version {
    VERSION=$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')
    VERSION=$(echo "${VERSION//./}")

    echo "INFO: Python version found: \"${VERSION}\"."
}

function install_python_if_necessary {
    if [ -z "${VERSION}" ] || [ "${VERSION}" != "2713" ]; then
        install_python_2.7.13
    fi
}

function install_python_2.7.13 {
    echo "INFO: Installing Python 2.7.13."
    install_build_dependencies
    get_python_sources_and_compile
    remove_python_sources
}

function install_build_dependencies {
    echo "INFO: Installing build dependencies."
    sudo apt-get install -y autotools-dev blt-dev bzip2 dpkg-dev g++-multilib gcc-multilib libbluetooth-dev libbz2-dev \
    libexpat1-dev libffi-dev libffi6 libffi6-dbg libgdbm-dev libgpm2 libncursesw5-dev libreadline-dev libsqlite3-dev \
    libssl-dev libtinfo-dev mime-support net-tools netbase python-crypto python-mox3 python-pil python-ply quilt tk-dev \
    zlib1g-dev python-virtualenv
}

function get_python_sources_and_compile {
    echo "INFO: Getting Python sources and compiling it."
    # Download
    wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
    # Unpack
    tar xfz Python-2.7.13.tgz
    # Configure
    cd Python-2.7.13/
    ./configure --prefix /usr/local/lib/python2.7.13 --enable-ipv6
    # Build
    make
    # Deploy
    sudo make install
    # Back to previous directory
    cd ..
}

function remove_python_sources {
    echo "INFO: Removing Python sources used during the installation."
    rm -rf Python-2.7.13
    rm Python-2.7.13.tgz
}

function create_virtualenv {
    # If the virtualenv directory already exists, cleans this directory
    if [ -d pyEnv ]; then
        echo "INFO: Virtual environment \"pyEnv\" found. Cleaning it up."
        sudo rm -rf pyEnv
    fi

    # Create virtualenv.
    echo "Creating the virtual environment \"pyEnv\"."
    virtualenv --python=/usr/local/lib/python2.7.13/bin/python pyEnv
}

function install_dependencies {
    echo "INFO: Activating virtualenv and installing all dependencies."
    . pyEnv/bin/activate
    pip install -r dependencies
    deactivate
}

go_to_source_directory
found_python_version
install_python_if_necessary
create_virtualenv
install_dependencies
