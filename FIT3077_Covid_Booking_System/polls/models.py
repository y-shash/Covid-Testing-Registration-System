from django.db import models


class User(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    givenName = models.CharField(max_length=200)
    familyName = models.CharField(max_length=200)
    userName = models.CharField(max_length=200)
    phoneNumber = models.IntegerField(default=0)
    isCustomer = models.BooleanField(default=False)
    isReceptionist = models.BooleanField(default=False)
    isHealthcareWorker = models.BooleanField(default=False)
    bookings = []
    additionalInfo = {}
