from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('detail/', views.account_detail, name='account_detail'),
    path('change-pin/', views.change_pin, name='change_pin'),
]
