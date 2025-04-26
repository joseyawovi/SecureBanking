from django.urls import path
from . import views

app_name = 'kyc'

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('status/', views.kyc_status, name='kyc_status'),
]
