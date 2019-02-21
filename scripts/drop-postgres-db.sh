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

# Delete migrations
echo
echo
echo delete migrations
find ./django_container/app -path "*/migrations/*.py" -not -name "__init__.py" -delete
find ./django_container/app -path "*/migrations/*.pyc"  -delete

# Stop pgadmin4
echo
echo stop pgadmin4
sudo docker-compose stop pgadmin4

# Drop the database
echo
echo drop database
sudo docker-compose exec --user postgres postgres dropdb clickgestion

# Recreate the database
echo
echo recreate database
sudo docker-compose exec --user postgres postgres createdb clickgestion

# Start pgadmin4
echo
echo start pgadmin4
sudo docker-compose start pgadmin4
