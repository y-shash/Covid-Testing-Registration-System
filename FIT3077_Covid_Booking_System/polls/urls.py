from django.urls import path
from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'measurements'

# save all the url paths that exist for the system
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='calculate-view'),
    # path('forms/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('booking/', views.booking, name='reception'),
    path('form/', views.form, name='form'),
    path('testsites/', views.testSites, name='testsites'),
]