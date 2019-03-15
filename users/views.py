from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import UserSignupForm
from users.mixins import UserHasAlreadSignup
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = '/'


class UserSignupView(UserHasAlreadSignup, CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('battles:create_battle')
