from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from accounts.models import UserProfile
from transactions.models import Transaction

from scoring.features import extract_features
from scoring.models import calculate_credit_score, credit_decision
from scoring.explain import explain_score
from scoring.loan_engine import generate_loan_offer

@api_view(["GET"])
def credit_score_view(request, profile_id):
    try:
        profile = UserProfile.objects.get(id=profile_id)
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    features = extract_features(profile)
    score = calculate_credit_score(features)
    decision = credit_decision(score)
    explanation = explain_score(features)

    return Response({
        "user": profile.user.username,
        "persona": profile.persona,
        "credit_score": score,
        "decision": decision,
        "explanation": explanation,
        "features_used": features,
    })

@api_view(["GET"])
def credit_dashboard(request, profile_id):
    try:
        profile = UserProfile.objects.get(id=profile_id)
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    transactions = Transaction.objects.filter(user_profile=profile)

    features = extract_features(profile)
    score = calculate_credit_score(features)
    decision = credit_decision(score)

    loan_offer = generate_loan_offer(score, profile.persona)

    return Response({
        "user": profile.user.username,
        "persona": profile.persona,
        "credit_score": score,
        "decision": decision,
        "loan_offer": loan_offer,
        "features": features,
        "total_transactions": transactions.count()
    })