from django.db import models
from django.contrib.auth.models import User


# GP related data
class GP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.CharField(max_length=200)

    def __str__(self):
        return 'GP Name: {}'.format(self.user.last_name)


# Specialist related data
class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'GP Name: {} {}'.format(self.user.first_name, self.user.last_name)
