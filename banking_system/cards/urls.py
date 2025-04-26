from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.card_list, name='card_list'),
    path('create/', views.create_card, name='create_card'),
    path('<int:card_id>/', views.card_detail, name='card_detail'),
    path('<int:card_id>/fund/', views.fund_card, name='fund_card'),
    path('<int:card_id>/withdraw/', views.withdraw_from_card, name='withdraw_from_card'),
    path('<int:card_id>/deactivate/', views.deactivate_card, name='deactivate_card'),
]
