# URLs de users
from django.conf.urls import url  # noqa

from users.views import UserLoginView, UserLogoutView, UserSignupView


app_name = 'users'

urlpatterns = [
    url(r'^login/', UserLoginView.as_view(), name='login'),
    url(r'^logout/', UserLogoutView.as_view(), name='logout'),
    url(r'^signup/', UserSignupView.as_view(), name='signup'),
]
