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


class Booking(models.Model):
    customerId = models.CharField(max_length=200)
    testingSiteId = models.CharField(max_length=200)
    startTime = models.DateTimeField()
    notes = models.CharField(max_length=200)
    additionalInfo = {}


class Measurement(models.Model):
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Distance from {self.location} to {self.destination} is {self.distance} km"
