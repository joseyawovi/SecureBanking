from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_id', 'transaction_type', 'amount', 'account', 'recipient_account', 'status', 'timestamp')
    list_filter = ('transaction_type', 'status', 'timestamp')
    search_fields = ('reference_id', 'account__account_number', 'recipient_account__account_number', 'description')
    readonly_fields = ('reference_id', 'timestamp')
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('reference_id', 'transaction_type', 'amount', 'description')
        }),
        ('Accounts', {
            'fields': ('account', 'recipient_account')
        }),
        ('Status', {
            'fields': ('status', 'failure_reason')
        }),
        ('Timestamps', {
            'fields': ('timestamp',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent direct creation of transactions through admin
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of transactions
        return False
