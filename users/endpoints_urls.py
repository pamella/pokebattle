from django.conf.urls import url

from users.endpoints import ListUserEndpoint


app_name = 'users'

urlpatterns = [
    url(r'^users/$', ListUserEndpoint.as_view(), name='list_user_endpoint'),

]
