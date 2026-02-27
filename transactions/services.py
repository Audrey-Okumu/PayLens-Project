import random
from datetime import datetime, timedelta
from .models import Transaction

def get_persona_rules(persona):
    """Return transaction behavior settings for each persona"""
    if persona == 'FARMER':
        return {
            'income_freq': 7,       # income every 7 days
            'income_amount': (5000, 15000),
            'expense_amount': (1000, 5000),
            'expense_freq': 5,
            'savings_freq': 2,
            'savings_amount': (500, 2000),
            'failure_rate': 0.05   #probability of transaction failue
        }
    elif persona == 'BODABODA':
        return {
            'income_freq': 1,
            'income_amount': (500, 2000),
            'expense_amount': (100, 500),
            'expense_freq': 1,
            'savings_freq': 1,
            'savings_amount': (50, 200),
            'failure_rate': 0.1
        }
    elif persona == 'SMALL_SHOP':
        return {
            'income_freq': 1,
            'income_amount': (1000, 5000),
            'expense_amount': (500, 3000),
            'expense_freq': 2,
            'savings_freq': 3,
            'savings_amount': (200, 1000),
            'failure_rate': 0.03
        }
    elif persona == 'STUDENT':
        return {
            'income_freq': 14,
            'income_amount': (2000, 4000),
            'expense_amount': (500, 1500),
            'expense_freq': 3,
            'savings_freq': 1,
            'savings_amount': (100, 300),
            'failure_rate': 0.15
        }
    
def generate_transactions_for(user_profile, days=90):
    """Generate a transaction history for the user based on persona rules"""
    rules = get_persona_rules(user_profile.persona)
    transactions = []

    start_date = datetime.now() - timedelta(days=days)

    for day_offset in range(days):
        date = start_date + timedelta(days=day_offset)

        # Income
        if day_offset % rules['income_freq'] == 0:
            amount = random.randint(*rules['income_amount'])
            status = 'FAILED' if random.random() < rules['failure_rate'] else 'SUCCESS'
            transactions.append(Transaction(
                user_profile=user_profile,
                amount=amount,
                transaction_type='INCOME',
                status=status,
                timestamp=date
            ))

        # Expenses
        if day_offset % rules['expense_freq'] == 0:
            amount = random.randint(*rules['expense_amount'])
            status = 'FAILED' if random.random() < rules['failure_rate'] else 'SUCCESS'
            transactions.append(Transaction(
                user_profile=user_profile,
                amount=amount,
                transaction_type='EXPENSE',
                status=status,
                timestamp=date
            ))

        # Savings
        if day_offset % rules['savings_freq'] == 0:
            amount = random.randint(*rules['savings_amount'])
            status = 'FAILED' if random.random() < rules['failure_rate'] else 'SUCCESS'
            transactions.append(Transaction(
                user_profile=user_profile,
                amount=amount,
                transaction_type='SAVINGS',
                status=status,
                timestamp=date
            ))

    # Bulk create
    Transaction.objects.bulk_create(transactions)
    return len(transactions)