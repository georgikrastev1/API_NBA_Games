"""
ASGI config for Django_Test_API_for_NBA_Gamer_Data project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Test_API_for_NBA_Gamer_Data.settings')

application = get_asgi_application()
