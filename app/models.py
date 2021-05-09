from django.db import models

# Create your models here.
class Users(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=10)

class UserAuthTokens(models.Model):
    email = models.CharField(max_length=50)
    token = models.CharField(max_length=200)
    timestamp = models.CharField(max_length=50)
