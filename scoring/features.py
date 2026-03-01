from transactions.models import Transaction
from django.db.models import Sum
import statistics

def extract_features(user_profile):
    txs = Transaction.objects.filter(user_profile=user_profile)

    income = txs.filter(transaction_type='INCOME', status='SUCCESS')
    expenses = txs.filter(transaction_type='EXPENSE', status='SUCCESS')
    savings = txs.filter(transaction_type='SAVINGS', status='SUCCESS')
    failed = txs.filter(status='FAILED')

    income_amounts = list(income.values_list('amount', flat=True))

    features = {
        "total_income": sum(income_amounts) if income_amounts else 0,
        "total_expenses": expenses.aggregate(Sum('amount'))['amount__sum'] or 0,
        "transaction_count": txs.count(),
        "failed_tx_rate": failed.count() / txs.count() if txs.exists() else 0,
        "income_consistency": (
            statistics.pstdev(income_amounts)
            if len(income_amounts) > 1 else 0
        ),
        "savings_ratio": (
            (savings.aggregate(Sum('amount'))['amount__sum'] or 0) /
            (sum(income_amounts) or 1)
        )
    }

    return features