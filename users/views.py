from django.contrib.auth.views import LoginView, LogoutView


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = '/'
