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
echo "           Getting $projectname django translations"
echo

# Check user is root
check_errs $EUID "This script must be run as root"


# Make messages
echo
echo
echo Making translation file
sudo docker-compose exec django python3 manage.py makemessages -a
check_errs $? "Failed making translations"


# Done
echo
echo
echo 'Translations done'
