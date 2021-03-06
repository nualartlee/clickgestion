#!/usr/bin/env python
import os

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

    # Make migrations
    execute_from_command_line(['manage.py', 'makemigrations'])

    # Migrate
    execute_from_command_line(['manage.py', 'migrate'])

    # Collect static files
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

    # Create default models
    from clickgestion.core.model_creation import create_default_models, create_test_models
    print('Creating default models')
    create_default_models()
    print('Creating test models')
    create_test_models()
    #from django.conf import settings
    #if settings.DEBUG:
        #print('Creating test models')
        #create_test_models()
