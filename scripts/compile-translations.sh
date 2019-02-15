#!/usr/bin/env bash

# Compile django's translated messages

# Work from projects's directory
cd "${0%/*}/.."

# Import common functions
source deploy-scripts/common.sh

# Assume the project's name is the same as the containing directory
projectname=${PWD##*/}

# Print header
echo "============================================================="
echo "           Compiling $projectname django translations"
echo

# Check user is root
check_errs $EUID "This script must be run as root"

# Compile messages
echo
echo
echo Compiling translations
sudo docker-compose exec django python3 manage.py compilemessages
check_errs $? "Failed compiling translations"


# Done
echo
echo
echo 'Translations compiled'
