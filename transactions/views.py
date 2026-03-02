import random
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import UserProfile
from .models import Transaction


@api_view(["POST"])
def simulate_mobile_money(request):
    profile_id = request.data.get("profile_id")
    amount = request.data.get("amount")
    tx_type = request.data.get("transaction_type")

    profile = UserProfile.objects.get(id=profile_id)

    status = random.choices(
        ["SUCCESS", "FAILED"],
        weights=[0.9, 0.1]
    )[0]

    tx = Transaction.objects.create(
        user_profile=profile,
        amount=amount,
        transaction_type=tx_type,
        status=status
    )

    return Response({
        "message": "Mobile money request processed",
        "transaction_id": tx.id,
        "status": status
    })