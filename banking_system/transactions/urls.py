from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('transfer/', views.transfer_money, name='transfer_money'),
    path('history/', views.transaction_history, name='transaction_history'),
]
