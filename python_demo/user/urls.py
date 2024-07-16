from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.handle_user, name='user-fetch-details'),
    path('login', views.login, name='user-login'),
]