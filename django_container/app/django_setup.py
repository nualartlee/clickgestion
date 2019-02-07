#!/usr/bin/env python
import os
import sys

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
    # Migrate
    execute_from_command_line(['manage.py', 'migrate'])

    # Collect static files
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

    # Create default user
    print('\n')
    print('Creating default users:')
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Create admin user
    with open('/run/secrets/django_admin_user') as f:
        admin_user = f.readline().rstrip('\n')
    try:
        User.objects.get(username=admin_user)
        print("Admin user already exists")
    except:
        with open('/run/secrets/django_admin_email') as f:
            admin_email = f.readline().rstrip('\n')
        with open('/run/secrets/django_admin_pass') as f:
            admin_pass = f.readline().rstrip('\n')
        User.objects.create_superuser(admin_user, admin_email, admin_pass)
        print("Admin user created")
        print("{0} ({1})\n{2}".format(admin_user, admin_email, admin_pass))

    # Create test1 user
    try:
        User.objects.get(username='test1')
        print("test1 user already exists")
    except:
        User.objects.create_user('test1', 'test1@here.com', 'test1pass')
        print("test1 user created")






