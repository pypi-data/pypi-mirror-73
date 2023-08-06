from django.conf import settings

PROTOCOL = getattr(settings, 'ELASTIC_PROTOCOL', 'http')
HOST = getattr(settings, 'ELASTIC_HOST', 'localhost')
PORT = getattr(settings, 'ELASTIC_PORT', 9200)
USE_SSL = getattr(settings, 'ELASTIC_USE_SSL', False)
