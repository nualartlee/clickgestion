#!/usr/bin/env bash

# Creates passwords, keys, etc

# Work from projects's directory
cd "${0%/*}/.."

# Import common functions
source deploy-scripts/common.sh

# Loop until postgres container is ready
until docker-compose exec --user postgres postgres psql -l
do
    echo "Waiting for postgres container..."
    sleep 3
done
echo "Postgres container is ready"

# Loop until django container is ready
until docker-compose exec django echo "Django container ready"
do
    echo "Waiting for django container..."
    sleep 3
done
done

# Additional delay for assurance
sleep 5

# Run Django setup
echo
echo "Running django_setup.py"
docker-compose exec django python3 django_setup.py
check_errs $? "Failed setting up django"
