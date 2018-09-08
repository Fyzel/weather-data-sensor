#!/usr/bin/env bash

# Modified from Nathan Jones' scripts located at https://gist.github.com/nathanpjones/61680827d180e930848d

# Edit the PYDIR variable to be the virtual Python directory's name
PYDIR=venv

DIR=$(dirname $(readlink -f "${BASH_SOURCE}"))

if [ ! -f ${DIR}/${PYDIR}/bin/python ]; then
  echo "This script should be located in the project root directory"
  echo "and the virtual environment should be created."
else
  # Change python to run as root
  sudo chown -v root:root "$DIR/$PYDIR/bin/python"
  sudo chmod -v u+s "$DIR/$PYDIR/bin/python"
fi
