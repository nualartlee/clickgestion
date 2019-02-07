#!/usr/bin/env bash

# Reset the entire django database

# Work from projects's directory
cd "${0%/*}/.."

# Import common functions
source deploy-scripts/common.sh

# Assume the project's name is the same as the containing directory
projectname=${PWD##*/}

# Print header
echo "============================================================="
echo "           Resetting Django Database $projectname"
echo

# Check user is root
check_errs $EUID "This script must be run as root"

# Reset
docker-compose exec django python3 manage.py flush --no-input
docker-compose exec django python3 django_setup.py

