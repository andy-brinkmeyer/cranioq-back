from django.db import models
from django.contrib.auth import get_user_model


class Role(models.Model):
    """This model holds the available roles: "anon", "gp", "specialist"."""
    role = models.CharField(max_length=20)

    def __str__(self):
        return 'Role: {}'.format(self.role)


class Profile(models.Model):
    """This model extends the Django User model."""

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    title = models.CharField(max_length=20)
    clinic_name = models.CharField(max_length=100)
    clinic_street = models.CharField(max_length=200, blank=True)
    clinic_city = models.CharField(max_length=200, blank=True)
    clinic_postcode = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return 'User: {}'.format(self.user.email)
