from scoring.models import CreditHistory

def log_credit_change(profile, old_score, new_score, reason):
    if old_score != new_score:
        CreditHistory.objects.create(
            profile=profile,
            previous_score=old_score,
            new_score=new_score,
            reason=reason
        )