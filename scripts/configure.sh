#!/bin/bash

# Gets the current directory for the service configuration.
SCRIPTS_DIRECTORY="$(dirname "${BASH_SOURCE[0]}")"
HOME_DIRECTORY=`cd ${SCRIPTS_DIRECTORY}/.. && pwd`

cd ${HOME_DIRECTORY}

# If the virtualenv does not yet exist, create it.
if [ ! -d pyEnv ]; then
    virtualenv pyEnv
fi

# Activate virtualenv and install all dependencies.
. pyEnv/bin/activate
pip install -r requirements/common.txt
deactivate

