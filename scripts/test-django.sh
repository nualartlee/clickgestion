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
echo "           Testing $projectname django coverage"
echo

# Check user is root
check_errs $EUID "This script must be run as root"

# Execute unit tests
echo
echo
docker-compose exec django coverage run --source='.' manage.py test --settings=clickgestion.settings.production
check_errs $? "Django Test Failed"

# Report test coverage, fail under limit
echo
echo
limit=100
docker-compose exec django coverage report --fail-under $limit
check_errs $? "Django coverage test failed (less than $limit%)"

# Exit
echo "Django coverage test passed"
echo
echo
