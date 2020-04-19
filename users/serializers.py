from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='profile.title', read_only=True)
    role = serializers.CharField(source='profile.role.role', read_only=True)
    clinic_name = serializers.CharField(source='profile.clinic_name', read_only=True)
    clinic_street = serializers.CharField(source='profile.clinic_street', read_only=True)
    clinic_city = serializers.CharField(source='profile.clinic_city', read_only=True)
    clinic_postcode = serializers.CharField(source='profile.clinic_postcode', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'title', 'role', 'clinic_name', 'clinic_street',
                  'clinic_city', 'clinic_postcode']
