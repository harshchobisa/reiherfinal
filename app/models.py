from django.db import models

# Create your models here.
class Users(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=10)

class UserAuthTokens(models.Model):
    email = models.CharField(max_length=50)
    token = models.CharField(max_length=200)
    timestamp = models.CharField(max_length=50)

class Mentors(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    year = models.IntegerField()
    gender = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    mentorType = models.CharField(max_length=50)
    firstActivity = models.CharField(max_length=50)
    secondActivity = models.CharField(max_length=50)
    thirdActivity = models.CharField(max_length=50)
    fourthActivity = models.CharField(max_length=50)
    fifthActivity = models.CharField(max_length=50)

class Mentees(models.Model):
    email = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    year = models.IntegerField()
    gender = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    menteeType = models.CharField(max_length=50)
    firstActivity = models.CharField(max_length=50)
    secondActivity = models.CharField(max_length=50)
    thirdActivity = models.CharField(max_length=50)
    fourthActivity = models.CharField(max_length=50)
    fifthActivity = models.CharField(max_length=50)

