from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from accounts.models import UserProfile
from transactions.models import Transaction

from scoring.features import extract_features
from scoring.models import calculate_credit_score, credit_decision
from scoring.explain import explain_score
from loans.loan_engine import generate_loan_offer

# Credit Score API

@api_view(["GET"])
def credit_score_view(request, profile_id):
    try:
        profile = UserProfile.objects.get(id=profile_id)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    features = extract_features(profile)
    score = calculate_credit_score(features)
    decision = credit_decision(score)
    explanation = explain_score(features)

    # Update current score in database
    profile.current_credit_score = score
    profile.save()

    return Response({
        "user": profile.user.username,
        "persona": profile.persona,
        "credit_score": score,
        "decision": decision,
        "current_credit_score": profile.current_credit_score,
        "loan_offer": generate_loan_offer(score, profile.persona),
        "explanation": explanation,
        "features_used": features,
    })

# Credit Dashboard API

@api_view(["GET"])
def credit_dashboard(request, profile_id):
    try:
        profile = UserProfile.objects.get(id=profile_id)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    transactions = Transaction.objects.filter(user_profile=profile)
    features = extract_features(profile)
    score = calculate_credit_score(features)
    decision = credit_decision(score)

    # Update current score in database
    profile.current_credit_score = score
    profile.save()

    loan_offer = generate_loan_offer(score, profile.persona)

    return Response({
        "user": profile.user.username,
        "persona": profile.persona,
        "credit_score": score,
        "current_credit_score": profile.current_credit_score,
        "decision": decision,
        "loan_offer": loan_offer,
        "features": features,
        "total_transactions": transactions.count()
    })


@api_view(["GET"])
def credit_history_view(request, profile_id):
    try:
        profile = UserProfile.objects.get(id=profile_id)
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    history = profile.credit_history.order_by("-created_at")

    return Response([
        {
            "previous_score": h.previous_score,
            "new_score": h.new_score,
            "reason": h.reason,
            "date": h.created_at
        }
        for h in history
    ])