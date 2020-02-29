from django.db import models
from django.contrib.auth.models import User


# GO related data
class GP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.CharField(max_length=200)
