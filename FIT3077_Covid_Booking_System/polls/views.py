from django.shortcuts import render, redirect
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


class RAT(CovidTest, ABC):
    def getTimeTaken(self):
        return self.type + " takes" + " 15 mins"


class PCR(CovidTest, ABC):
    def getTimeTaken(self):
        return self.type + " takes" + " 72 hours"


class Login(object):
    def __init__(self, username):
        self.username = username
        self.id = ""

    def setId(self, id):
        self.id = id

    def getUserName(self):
        return self.username


class Form(object):
    def __init__(self, q1, q2, q3, q4, q5, q6):
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6

    def getTotalAnswers(self):
        return self.q1 + self.q2 + self.q3 + self.q4 + self.q5 + self.q6


# function

userId = ''


def login(request):
    system = System()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        login = Login(username)

        response = requests.post(
            url=system.getLogin(),
            headers={'Authorization': my_api_key},
            params={'jwt': 'true'},  # Return a JWT so we can use it in Part 5 later.
            data={
                'userName': username,
                'password': password
                # The password for each of the sample user objects that have been created for you are the same as their respective usernames.
            }
        )
        json_data = response.json()

        if "statusCode" not in json_data.keys():

            response = requests.get(url=system.getUsers(), headers={'Authorization': my_api_key})
            json_data = response.json()

            # The GET /user endpoint returns a JSON array, so we can loop through the response as we could with a normal array/list.

            for user in json_data:
                if user["userName"] == username:
                    global userId
                    login.setId(user['id'])
                    userId = user['id']
                    theUser = user

            if theUser['isReceptionist']:
                return redirect('/form')
            else:
                return redirect('/testsites')

        elif json_data['statusCode'] is 403:
            print('Credentials are invalid')
            return redirect('/login')

    return render(request, 'measurements/login.html')


def form(request):
    if request.method == "POST":
        q1 = int(request.POST.get('q1', False))
        q2 = int(request.POST.get('q2', False))
        q3 = int(request.POST.get('q3', False))
        q4 = int(request.POST.get('q4', False))
        q5 = int(request.POST.get('q5', False))
        q6 = int(request.POST.get('q6', False))

        form = Form(q1, q2, q3, q4, q5, q6)
        total = form.getTotalAnswers()

        if total > 3:
            test = "PCR"
        else:
            test = "RAT"

        messages.info(request, 'Test To Be Taken is a ' + test + " Test!")

    return render(request, 'measurements/form.html')


def booking(request):
    system = System()
    if request.method == "POST":
        testSite = request.POST['siteId']
        start = request.POST['startTime']
        start = start + ":00.000Z"
        home = request.POST.get('home', False)
        if home == 1:
            testType = "RAT"
        else:
            testType = "PCR"

        print(userId)

        response = requests.post(
            url=system.getBookings(),
            headers={'Authorization': my_api_key},
            params={'jwt': 'true'},  # Return a JWT so we can use it in Part 5 later.
            data={
                "customerId": userId,
                "testingSiteId": testSite,
                "startTime": start,
                "notes": testType,
                "additionalInfo": {}
                # The password for each of the sample user objects that have been created for you are the same as their respective usernames.
            }
        )
        json_data = response.json()
        print(json_data)
        return redirect('/testsites')

    return render(request, 'measurements/booking.html')


def testSites(request):
    system = System()
    response = requests.get(url=system.getTestingSites(), headers={'Authorization': my_api_key})
    json_data = response.json()
    headers = [["Name", "ID", "Suburb", "Phone Number", "Waiting Time", "Facility Type", "Book Now"]]
    for item in json_data:
        if "bookings" in item:
            item["bookingTime"] = len(item["bookings"]) * 30
        else:
            item["bookingTime"] = 0

    return_list = json_data

    if request.method == "POST":
        search_term = request.POST.get('search', False)
        return_list = []
        type = None
        for i in range(len(json_data)):
            if "type" in json_data[i]["additionalInfo"]:
                type = json_data[i]["additionalInfo"]["type"]
            if json_data[i]["address"]["suburb"].lower() == search_term.lower() or (
                    type is not None and json_data[i]["additionalInfo"]["type"].lower() == search_term.lower()):
                return_list.append(json_data[i])

    context = {'list': headers,
               'value': return_list}

    return render(request, 'measurements/testsites.html', context)
