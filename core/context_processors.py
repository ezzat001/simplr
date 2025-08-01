from django.core.cache import cache
from .models import ServerSetting 

def system_settings(request):
    settings = cache.get('system_settings')
    if not settings:
        settings = ServerSetting.objects.first()
        cache.set('system_settings', settings, 86400)  # cache for 24 hours
    return {'system_settings': settings}



