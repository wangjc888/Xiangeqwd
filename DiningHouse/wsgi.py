"""
WSGI config for DiningHouse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
# import sys

# path = '/path/to/DiningHouse/DiningHouse'
# if path not in sys.path:
#     sys.path.append(path)

# os.environ['DJANGO_SETTINGS_MODULE'] = "DiningHouse.settings"
# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DiningHouse.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = "DiningHouse.settings"
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-eggs'
application = get_wsgi_application()
