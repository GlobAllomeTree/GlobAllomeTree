
from django.conf import settings

#Context processor to pass settings that we need to the template
def template_settings(request):
    return {'search_url': settings.SEARCH_URL}