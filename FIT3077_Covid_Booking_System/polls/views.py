from django.core.mail.backends import console
from django.shortcuts import render, get_object_or_404, redirect
from .models import Measurement, User
from django.contrib.auth.models import auth
from .forms import MeasurementModelForm
from django.http import HttpResponse
from django.contrib import messages
import requests
from abc import ABC, abstractmethod

# NOTE: In order to access the web service, you will need to include your API key in the Authorization header of all requests you make.
# Your personal API key can be obtained here: https://fit3077.com
my_api_key = 'HRpTfcjTqdBqq76RWJqGdgJPtgK97q'

# Provide the root URL for the web service. All web service request URLs start with this root URL.
root_url = 'https://fit3077.com/api/v1'


# To get a specific resource from the web service, extend the root URL by appending the resource type you are looking for.
# For example: [root_url]/user will return a JSON array object containing all users.

class System(object):
    def __init__(self):
        self.users_url = root_url + "/user"
        self.users_login_url = root_url + "/user/login"
        self.testing_site_url = root_url + "/testing-site"
        self.booking_url = root_url + "/booking"
        self.covid_test_url = root_url + "/covid-test"
        self.photo_url = root_url + "/photo"

    def getUsers(self):
        return self.users_url

    def getLogin(self):
        return self.users_login_url

    def getTestingSites(self):
        return self.testing_site_url

    def getBookings(self):
        return self.booking_url

    def getCovidTests(self):
        return self.covid_test_url

    def getPhoto(self):
        return self.photo_url


class CovidTest(ABC):
    def __init__(self, type, patient, id, administerer):
        self.type = type
        self.patient = patient
        self.id = id
        self.administerer = administerer

    @abstractmethod
    def getCovidType(self):
        return self.type

    @abstractmethod
    def getId(self):
        return self.id

    @abstractmethod
    def getPatient(self):
        return self.patient

    @abstractmethod
    def getAdministerer(self):
        return self.administerer