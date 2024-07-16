from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_transactions, name='transaction-fetch-details'),
    path('transfer-money', views.transfer_money, name='transfer-money'),
    path('debit', views.debit_money, name='debit-money'),
    path('credit', views.credit_money, name='credit-money'),
]