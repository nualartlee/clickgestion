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

# Run selenium in a docker container
container_name=selenium
network_name=clickgestion_default

# Check if container already exists
existing=$(docker ps -a --format "{{.Names}}" | grep -w "$container_name")
running=$(docker ps --format "{{.Names}}" | grep -w "$container_name")
if [[ "$existing" == "$container_name" ]];
then
    # Run the existing container
    if [[ "$running" != "$container_name" ]];
    then
        echo "Starting existing selenium container"
        docker container start $container_name
    else
        echo "A selenium container is already running"
    fi
else
    # Start a new selenium docker container
    echo "Building new selenium container"
    docker run -d --net $network_name --name $container_name -p 5900:5900 -v /dev/shm:/dev/shm selenium/standalone-firefox-debug >/dev/null
fi

# Connect to network
docker network connect $network_name $container_name >/dev/null 2>&1

# Loop until selenium container is ready
until docker-compose exec django echo "Selenium container ready"
do
    echo "Waiting for selenium container..."
    sleep 3
done

# Execute functional tests
docker-compose exec django python3 clickgestion/core/functional_test.py
check_errs $? "Django Functional Tests Failed"

# Stop the container if it was not running initially
if [[ "$running" != "$container_name" ]];
then
    echo "Selenium container stopped"
    docker container stop $container_name
else
    echo "Selenium container left running"
fi


# Exit
echo "Django Functional Tests Passed"
echo
echo
