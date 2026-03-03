def generate_loan_offer(score, persona):
    if score < 50:
        return None

    base_amount = 5000 if persona == "FARMER" else 8000

    multiplier = score / 100

    return {
        "max_amount": round(base_amount * multiplier, 2),
        "interest_rate": 12 if score >= 70 else 18,
        "tenure_months": 6 if score >= 70 else 3
    }

def update_score_with_repayment(current_score, repayment):
    
    #Adjusts the credit score based on repayment behavior.   
    new_score = current_score

    if repayment.on_time:
        new_score += 5  # reward
    else:
        new_score -= 10  # penalty

    # Clamp between 0 and 100
    return max(0, min(new_score, 100))