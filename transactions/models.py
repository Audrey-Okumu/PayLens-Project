from django.db import models
from accounts.models import UserProfile

TRANSACTION_TYPE_CHOICES = [
    ('INCOME', 'Income'),
    ('EXPENSE', 'Expense'),
    ('SAVINGS', 'Savings'),
    ('BILL', 'Bill Payment')
]

STATUS_CHOICES = [
    ('SUCCESS', 'Success'),
    ('FAILED', 'Failed')
]

class Transaction(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user_profile.user.username} | {self.transaction_type} | {self.amount}"


