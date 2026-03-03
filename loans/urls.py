from django.urls import path
from .views import record_repayment

urlpatterns = [
    path('repayment/<int:loan_id>/', record_repayment, name='record_repayment'),
]