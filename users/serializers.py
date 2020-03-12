from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role.role', read_only=True)
    clinic_name = serializers.CharField(source='profile.clinic_name', read_only=True)
    clinic_address = serializers.CharField(source='profile.clinic_address', read_only=True)
    clinic_postcode = serializers.CharField(source='profile.clinic_postcode', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'clinic_name', 'clinic_address', 'clinic_postcode']
