# URLs de users
from django.conf.urls import url  # noqa

from users.views import UserLoginView, UserLogoutView


app_name = 'users'

urlpatterns = [
    url(r'^login/', UserLoginView.as_view(), name='login'),
    url(r'^logout/', UserLogoutView.as_view(), name='logout'),
]
