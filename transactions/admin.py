from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    #Controls which fields appear as columns in the transaction list view
    list_display = (
        'user_profile',
        'transaction_type',
        'amount',
        'status',
        'timestamp',
    )
    # Filtering Options
    list_filter = (
        'transaction_type',
        'status',
    )
    # Searchable fields
    search_fields = (
        'user_profile__user__username',
        'user_profile__phone_number',
    )
    # default descending order
    ordering = ('-timestamp',)
