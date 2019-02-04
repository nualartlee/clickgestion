#!/usr/bin/env python
"""
Django's manage.py with repeat after delay on failures.

Ugly hack to allow docker container dependencies time to run.
(PostgreSQL needs lots of time on first setup).

"""
import os
import sys
from time import sleep
import logging
import traceback

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clickgestion.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    # Make a few attempts
    sleep(5)
    attempts = 0
    while attempts < 5:
        try:
            attempts += 1
            print('{0} : Attempt {1}'.format(' '.join(sys.argv), attempts))
            logger.info('{0} : Attempt {1}'.format(' '.join(sys.argv), attempts))
            execute_from_command_line(sys.argv)
            attempts = 5
        except Exception as e:
            logger.error('ERROR: {0} : Attempt {1} Failed'.format(' '.join(sys.argv), attempts))
            if attempts == 4:
                raise
            else:
                sleep(3)
