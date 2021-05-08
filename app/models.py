from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=50);
    password = models.CharField(max_length=200);
    role = models.CharField(max_length=10);