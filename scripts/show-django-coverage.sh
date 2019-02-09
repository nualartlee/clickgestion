#!/usr/bin/env bash

# Test the django application

# Work from projects's directory
cd "${0%/*}/.."

# Import common functions
source deploy-scripts/common.sh

# Assume the project's name is the same as the containing directory
projectname=${PWD##*/}

# Get the owner of the project
projectowner=$(ls -ld $PWD | awk '{print $3}')

# Print header
echo "============================================================="
echo "           Testing $projectname django coverage"
echo

# Check user is root
check_errs $EUID "This script must be run as root"

# Execute unit tests
echo
echo
docker-compose exec django coverage run --source='.' manage.py test --settings=clickgestion.settings.production

# Generage html report
echo
echo
docker-compose exec django coverage html

# Display report in firefox
su $projectowner firefox ./django_container/app/htmlcov/index.html
