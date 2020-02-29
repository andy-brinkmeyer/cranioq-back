from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']

    @staticmethod
    def get_role(obj):
        if hasattr(obj, 'gp'):
            return 'gp'
        else:
            return 'anon'
