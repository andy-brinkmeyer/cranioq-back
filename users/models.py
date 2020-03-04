from django.db import models
from django.contrib.auth.models import User


# GP related data
class GP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.CharField(max_length=200)


# Specialist related data
class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
