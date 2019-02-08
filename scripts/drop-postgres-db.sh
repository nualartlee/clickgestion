#!/usr/bin/env bash

# Drop the database in the postgres container

# Work from projects's directory
cd "${0%/*}/.."

# Import common functions
source deploy-scripts/common.sh

# Assume the project's name is the same as the containing directory
projectname=${PWD##*/}

# Print header
echo "============================================================="
echo "           Dropping $projectname postgres database"
echo

# Check user is root
check_errs $EUID "This script must be run as root"

# Drop the database
sudo docker-compose exec --user postgres postgres dropdb clickgestion

# Drop the database
sudo docker-compose exec --user postgres postgres createdb clickgestion
