from rest_framework import serializers

from djangoAuthentication.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserProfile
        fields = ['id', 'nickname', 'username', 'password', 'email', 'desired_project']