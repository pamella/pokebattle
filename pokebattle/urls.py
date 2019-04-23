from django.conf import settings
from django.conf.urls import include, url  # noqa
from django.contrib import admin
from django.views.generic import TemplateView

import django_js_reverse.views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),

    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'', include('battles.urls', namespace='battles')),
    url(r'', include('users.urls')),

    url(r'social/', include('social_django.urls', namespace='social')),
    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'api/', include('battles.endpoints_urls', namespace='api_battles')),
    url(r'api/', include('pokemons.endpoints_urls', namespace='api_pokemon')),
    url(r'api/', include('users.endpoints_urls', namespace='api_user')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
