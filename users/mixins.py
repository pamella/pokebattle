from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

from users.models import User


class UserHasAlreadSignup(UserPassesTestMixin):
    permission_denied_message = "User, you've already signup."
    redirect_field_name = None

    def test_func(self):
        user = self.request.user
        if User.objects.filter(id=user.id).exists():
            return False
        return True

    def handle_no_permission(self):
        return redirect('users:logout')
