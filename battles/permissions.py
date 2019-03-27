from rest_framework import permissions


class IsTrainerInBattle(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user in [obj.trainer_creator, obj.trainer_opponent]
