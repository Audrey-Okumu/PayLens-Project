from django.contrib import admin
from .models import UserProfile
from transactions.services import generate_transactions_for

@admin.action(description="Generate mobile money transactions (90 days)")
def generate_transactions(modeladmin, request, queryset):
    for profile in queryset:
        generate_transactions_for(profile, days=90)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'persona', 'phone_number', 'current_credit_score', 'date_joined')
    actions = [generate_transactions]