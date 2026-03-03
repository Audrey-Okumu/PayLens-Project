from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Loan, Repayment
from scoring.models import calculate_credit_score, credit_decision
from scoring.features import extract_features
from .loan_engine import update_score_with_repayment , generate_loan_offer

@api_view(["POST"])
def record_repayment(request, loan_id):
    """
    Record a repayment and update user's credit score
    """
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

    amount = request.data.get("amount")
    if amount is None:
        return Response({"error": "Repayment amount is required"}, status=status.HTTP_400_BAD_REQUEST)

    on_time = request.data.get("on_time", True)

    repayment = Repayment.objects.create(
        loan=loan,
        amount=amount,
        on_time=on_time
    )

    profile = loan.user_profile
    features = extract_features(profile)
    score = calculate_credit_score(features)
    score = update_score_with_repayment(score, repayment)
    decision = credit_decision(score)

    # Update the user's current score in the database
    profile.current_credit_score = score
    profile.save()

    return Response({
        "message": "Repayment recorded",
        "repayment_amount": amount,
        "on_time": on_time,
        "updated_score": score,
        "current_credit_score": profile.current_credit_score,
        "decision": decision,
        "loan_offer": generate_loan_offer(score, profile.persona)
    })