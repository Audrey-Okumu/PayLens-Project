def explain_score(features):
    explanations = []

    if features['failed_tx_rate'] > 0.1:
        explanations.append("High rate of failed transactions")

    if features['savings_ratio'] > 0.1:
        explanations.append("Consistent savings behavior")

    if features['income_consistency'] < 2000:
        explanations.append("Stable income pattern")

    if not explanations:
        explanations.append("Limited transaction history")

    return explanations