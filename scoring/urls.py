from django.urls import path
from .views import credit_score_view

urlpatterns = [
    path("credit-score/<int:profile_id>/", credit_score_view),
]