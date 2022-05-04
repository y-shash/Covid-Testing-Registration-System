from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from abc import abstractmethod, ABC

# NOTE: In order to access the web service, you will need to include your API key in the Authorization header of all requests you make.
# Your personal API key can be obtained here: https://fit3077.com
my_api_key = 'HRpTfcjTqdBqq76RWJqGdgJPtgK97q'

# Provide the root URL for the web service. All web service request URLs start with this root URL.
root_url = 'https://fit3077.com/api/v1'


# To get a specific resource from the web service, extend the root URL by appending the resource type you are looking for.
# For example: [root_url]/user will return a JSON array object containing all users.

class System(object):
    """
    class to store all the necessary URLs of the application and get each as using a public method keeping
    the URLS private and unchangeable
    """

    def __init__(self):
        self.users_url = root_url + "/user"
        self.users_login_url = root_url + "/user/login"
        self.testing_site_url = root_url + "/testing-site"
        self.booking_url = root_url + "/booking"
        self.covid_test_url = root_url + "/covid-test"
        self.photo_url = root_url + "/photo"
        self.login = ""
        self.form = ""

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

    def setLogin(self, login):
        self.login = login

    def setForm(self, form):
        self.form = form


class Search(object):
    """
    class to store the word that user has entered as a search word and filter
    """

    def __init__(self, search):
        self.search = search

    def getSearch(self):
        return self.search


class CovidTest:
    """
    Abstract class to create different all the different types of tests, and to extend the similar
    basic functions for all the different test types
    """

    def __init__(self, patient, id):
        self.patient = patient
        self.id = id
        self.administerer = ""

    @abstractmethod
    def getId(self):
        return self.id

    @abstractmethod
    def getPatient(self):
        return self.patient

    @abstractmethod
    def getAdministerer(self):
        return self.administerer

    @abstractmethod
    def setAdministerer(self, administerer):
        self.administerer = administerer

    @abstractmethod
    def getType(self):
        pass


class RAT(CovidTest):
    """
    class for created RAT test instances
    """

    def getTimeTaken(self):
        return self.type + " takes" + " 15 mins"

    def getType(self):
        return "RAT"


class PCR(CovidTest):
    """
        class for created RAT test instances
        """

    def getTimeTaken(self):
        return self.type + " takes" + " 72 hours"

    def getType(self):
        return "PCR"


class Login(object):
    """
    class to create a login object to store the users details once they log in to the system
    and used to get the users' data when required
    """

    def __init__(self, username):
        self.username = username
        self.id = ""

    def setId(self, id):
        self.id = id

    def getUserName(self):
        return self.username


class Customer:
    """
    class to create abstract class for all possible customers that are can be in the system
    """

    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    @abstractmethod
    def getId(self):
        return self.id

    @abstractmethod
    def getRole(self):
        return self.role


class Patient(Customer, ABC):
    """class for patients"""
    pass


class Administerer(Customer, ABC):
    """class for administers"""
    pass


class Administrator(Customer, ABC):
    """class for administrators"""
    pass


class Form(object):
    """
    class to store all the data regarding the form in the system and the answers that have been given by the user
    to it.
    """

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
administerer = ''
patient = ''


def login(request):
    """
    all the functionality for logging in and checking if the user that has logged in is a customer or an
    administerer, if he is an administerer it will sned him/her to the form page to request the details
    from the user who is onsite, we also assume the administerer knows the site ID at where he/she is.
    :param request: the request for logging sent from the site
    :return: the page that has to be render depending on the outcome of the login
    """
    system = System()
    if request.method == "POST":
        # get the username and the password of the user
        username = request.POST['username']
        password = request.POST['password']
        login = Login(username)
        system.setLogin(login)

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

        # check the status of the login attempt
        if "statusCode" not in json_data.keys():

            response = requests.get(url=system.getUsers(), headers={'Authorization': my_api_key})
            json_data = response.json()

            # The GET /user endpoint returns a JSON array, so we can loop through the response as we could with a normal array/list.
            global userId
            # if the users' username exists in the list of usernames
            for user in json_data:
                # save their ID for future booking purposes
                if user["userName"] == username:
                    login.setId(user['id'])
                    userId = user['id']
                    theUser = user

            # if they are a receptionist send them to the form page

            if theUser['isReceptionist']:
                global administerer
                administerer = Administerer(userId, username, "receptionist")
                return redirect('/form')
            # else if they are a customer send them to the testing sites table page
            else:
                global patient
                patient = Patient(userId, username, "patient")
                return redirect('/testsites')

        # if the status code for the login is an incorrect entry sshow a message stating that the
        # credentials are invalid
        elif json_data['statusCode'] is 403:
            messages.info(request, "Credentials are invalid")
            return redirect('/login')

        elif json_data['statusCode'] is 404:
            messages.info(request, "Credentials are invalid")
            return redirect('/login')

    return render(request, 'measurements/login.html')


def form(request):
    """
    uses the UI forms input data to check whether the users symptoms are severe
    and recommend to either get a PCR or RAT test.
    :param request: the request from the site being handled
    :return: the render of the form html
    """
    system = System()
    if request.method == "POST":
        # get all the values from all the questions
        q1 = int(request.POST.get('q1', False))
        q2 = int(request.POST.get('q2', False))
        q3 = int(request.POST.get('q3', False))
        q4 = int(request.POST.get('q4', False))
        q5 = int(request.POST.get('q5', False))
        q6 = int(request.POST.get('q6', False))

        # check how many symptoms the user has
        form = Form(q1, q2, q3, q4, q5, q6)
        total = form.getTotalAnswers()
        system.setForm(form)

        # if user has more than 3 symptoms recommend a PCR
        if total > 3:
            test = "PCR"
        # if 3 or fewer symptoms recommend a RAT
        else:
            test = "RAT"

        messages.info(request, 'Test To Be Taken is a ' + test + " Test!")

    return render(request, 'measurements/form.html')


def booking(request):
    """
    creates a booking using the information provided by the user or receptionist.
    They will enter the Testing Site's ID and the start time for the booking and also
    mark whether the booking is for a home test or on site.;
    :param request: the request from front end being handled
    :return: the render of the booking page
    """
    system = System()
    if request.method == "POST":
        # save the data about the site ID and start time for the booking
        testSite = request.POST['siteId']
        patientFormId = request.POST['customerId']
        start = request.POST['startTime']
        start = start + ":00.000Z"
        # check if it's an onsite or home test
        home = request.POST.get('home', False)

        global patient
        global administerer

        # if administerer is logged in she will know your ID
        if patient == '':
            patientId = patientFormId
            administererId = administerer.getId()
        # if patient is logged in he is at home and administerer is yet unknown
        else:
            administererId = ""
            patientId = patient.getId()

        if home == 1:
            testType = RAT(patient, patientId)
        else:
            testType = PCR(patient, patientId)

        response = requests.post(
            url=system.getBookings(),
            headers={'Authorization': my_api_key},
            params={'jwt': 'true'},  # Return a JWT so we can use it in Part 5 later.
            data={
                "customerId": userId,
                "testingSiteId": testSite,
                "startTime": start,
                "notes": testType.getType(),
                "additionalInfo": {}
                # The password for each of the sample user objects that have been created for you are the same as their respective usernames.
            }
        )
        json_data = response.json()

        # after a booking is created a Covid test for the booking is also created
        response = requests.post(
            url=system.getCovidTests(),
            headers={'Authorization': my_api_key},
            params={'jwt': 'true'},  # Return a JWT so we can use it in Part 5 later.
            data={
                "type": testType,
                "patientId": patientId,
                "administererId": administererId,
                "bookingId": json_data["id"],
                "result": "PENDING",
                "status": "CREATED",
                "notes": "",
                "additionalInfo": {}
                # The password for each of the sample user objects that have been created for you are the same as their respective usernames.
            }
        )

        json_data = response.json()

        return redirect('/testsites')

    return render(request, 'measurements/booking.html')


def testSites(request):
    """
    retrieves and passes all the values needed by the sites table to the front end render of the sites table
    also has the functionality for the search bar which will store the search word and check if it matches a word
    in the suburbs of every site or their additional info which stores the type of facility they are.
    :param request: the request that is sent by the front end to show the table
    :return: the render of the table in the test site page
    """
    system = System()
    response = requests.get(url=system.getTestingSites(), headers={'Authorization': my_api_key})
    json_data = response.json()
    # store the headers for the table
    headers = [["Name", "ID", "Suburb", "Phone Number", "Waiting Time", "Facility Type", "Book Now"]]

    # calculate the booking time for each of the sites using the number of bookings they have in them
    for item in json_data:
        if "bookings" in item:
            item["bookingTime"] = len(item["bookings"]) * 30
        else:
            item["bookingTime"] = 0

    return_list = json_data
    global userId
    global patient
    global administerer

    # if administerer is logged in she will know your ID
    if patient == '':
        userId = administerer.getId()
    # if patient is logged in he is at home and administerer is yet unknown
    else:
        userId = patient.getId()
    # if search is clicked
    if request.method == "POST":
        search_term = request.POST.get('search', False)
        return_list = []
        type = None
        # check all the sites information
        for i in range(len(json_data)):
            # check all the types in the given facility
            if "type" in json_data[i]["additionalInfo"]:
                type = json_data[i]["additionalInfo"]["type"]
            # check if the suburb for the site matches the search word
            if json_data[i]["address"]["suburb"].lower() == search_term.lower():
                return_list.append(json_data[i])
            # checkl the types in the facility to check if one matches the search word
            elif type is not None:
                for item in type:
                    if item.lower() == search_term.lower():
                        return_list.append(json_data[i])

    context = {'list': headers,
               'value': return_list,
               'id': userId}

    return render(request, 'measurements/testsites.html', context)
