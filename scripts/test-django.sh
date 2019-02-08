#!/usr/bin/env bash

# Test the django application

# Work from projects's directory
cd "${0%/*}/.."

# Import common functions
source deploy-scripts/common.sh

# Assume the project's name is the same as the containing directory
projectname=${PWD##*/}

# Print header
echo "============================================================="
echo "           Testing $projectname django application"
echo

# Check user is root
check_errs $EUID "This script must be run as root"

# Test
echo
echo
echo test
docker-compose exec django python3 manage.py test --settings=clickgestion.settings.production
