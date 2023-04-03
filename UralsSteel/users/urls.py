from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'users'
urlpatterns = [
    path('registration/', registration, name='registration'),
    path('authorisation/', login, name='authorisation'),
    path('logout/', logout, name='logout')
]