from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/kyc/<int:document_id>/verify/', views.verify_kyc_document, name='verify_kyc_document'),
]
