#!/usr/bin/env bash

# Creates passwords, keys, etc

# Work from projects's directory
cd "${0%/*}/.."

# Import common functions
source deploy-scripts/common.sh

# Run Scrapy setup
echo
echo "Running scrapyd_setup.sh"
docker-compose exec scrapyd ./scrapyd_setup.sh
check_errs $? "Failed setting up scrapyd"

# Run Django setup
echo
echo "Running django_setup.py"
docker-compose exec django python3 django_setup.py
check_errs $? "Failed setting up django"
