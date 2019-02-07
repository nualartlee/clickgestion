#!/usr/bin/env bash

# Restart the uwsgi serving Django

# Work from projects's directory
cd "${0%/*}/.."

# Import common functions
source deploy-scripts/common.sh

# Assume the project's name is the same as the containing directory
projectname=${PWD##*/}

# Print header
echo "============================================================="
echo "           Restarting uwsgi serving $projectname"
echo

# Check user is root
check_errs $EUID "This script must be run as root"

# Reset
docker-compose exec django kill -HUP 1
