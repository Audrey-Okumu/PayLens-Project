from django.urls import path
from .views import simulate_mobile_money

urlpatterns = [
    path("mobile-money/", simulate_mobile_money),
]