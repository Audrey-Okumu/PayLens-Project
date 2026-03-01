from decimal import Decimal

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