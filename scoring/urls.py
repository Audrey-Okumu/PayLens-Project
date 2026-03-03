from django.urls import path
from .views import credit_score_view ,credit_dashboard , credit_history_view

urlpatterns = [
    path("credit-score/<int:profile_id>/", credit_score_view),
    path("dashboard/<int:profile_id>/", credit_dashboard),
    path("credit-history/<int:profile_id>/", credit_history_view),
]