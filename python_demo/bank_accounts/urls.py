from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.handle_bank_account, name='handle-bank-accounts'),
    path('health-check/', views.health_check, name='bank-account-health-check'),
]   