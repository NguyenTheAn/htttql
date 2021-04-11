from django.db import models
import random

# Create your models here.
class User(models.Model):
    userID = models.IntegerField(primary_key = True)
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 100, default=None, blank=True, null=True)
    email = models.CharField(max_length = 100, default=None, blank=True, null=True)
    address = models.CharField(max_length = 100, default=None, blank=True, null=True)
    sex = models.BooleanField(default=None)