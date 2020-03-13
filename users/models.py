from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    role = models.CharField(max_length=20)

    def __str__(self):
        return 'Role: {}'.format(self.role)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    clinic_name = models.CharField(max_length=100)
    clinic_address = models.CharField(max_length=200, blank=True)
    clinic_postcode = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return 'User: {}'.format(self.user.email)
