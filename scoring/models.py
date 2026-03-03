from decimal import Decimal
from django.db import models
from accounts.models import UserProfile

def calculate_credit_score(features):
    score = 50  # baseline

    if features['total_income'] > Decimal("50000"):
        score += 15

    if features['failed_tx_rate'] < 0.1:
        score += 15
    else:
        score -= 10

    if features['savings_ratio'] > Decimal("0.1"):
        score += 10

    if features['income_consistency'] < Decimal("2000"):
        score += 10
    else:
        score -= 5

    return max(0, min(score, 100))


def credit_decision(score):
    if score >= 70:
        return "APPROVED"
    elif score >= 50:
        return "REVIEW"
    else:
        return "REJECTED"

class CreditHistory(models.Model):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="credit_history"
    )
    previous_score = models.IntegerField()
    new_score = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username}: {self.previous_score} → {self.new_score}"