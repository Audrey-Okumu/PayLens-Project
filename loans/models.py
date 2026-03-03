from django.db import models
from accounts.models import UserProfile

class Loan(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("PAID", "Paid"),
        ("DEFAULTED", "Defaulted"),
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure_months = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.amount} - {self.status}"
    
class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateTimeField(auto_now_add=True)
    on_time = models.BooleanField(default=True)  # True if repayment within due date

    def __str__(self):
        return f"{self.loan.user_profile.user.username} - {self.amount} - {'On time' if self.on_time else 'Late'}"
