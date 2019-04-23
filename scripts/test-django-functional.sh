#!/usr/bin/env bash

# Run django application functional tests

# Work from projects's directory
cd "${0%/*}/.."

# Import common functions
source deploy-scripts/common.sh

# Assume the project's name is the same as the containing directory
projectname=${PWD##*/}

# Print header
echo "============================================================="
echo "           $projectname django functional test"
echo

# Check user is root
check_errs $EUID "This script must be run as root"

# Stop and remove any old selenium containers
name=selenium
running=$(docker ps --format "{{.Names}}" | grep -w "$name")
if [[ "$running" == "$name" ]];
then
    docker stop $name >/dev/null
    docker rm $name >/dev/null
fi
# Start a new selenium docker container
docker run -d --net clickgestion_default --name $name -v /dev/shm:/dev/shm selenium/standalone-firefox:3.141.59-mercury >/dev/null
check_errs $? "Failed deploying selenium container for tests"
echo "Selenium container built"

# Loop until selenium container is ready
until docker-compose exec django echo "Selenium container ready"
do
    echo "Waiting for selenium container..."
    sleep 3
done

# Execute functional tests
docker-compose exec django python3 clickgestion/core/functional_test.py
check_errs $? "Django Functional Tests Failed"

# Exit
echo "Django Functional Tests Passed"
echo
echo
