from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_number_masked', 'user', 'card_type', 'is_active', 'expiry_date', 'created_at')
    list_filter = ('card_type', 'is_active', 'created_at')
    search_fields = ('user__email', 'user__full_name', 'card_number')
    readonly_fields = ('card_number', 'cvv', 'created_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Card Details', {
            'fields': ('card_number', 'card_type', 'expiry_date', 'cvv', 'balance')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def card_number_masked(self, obj):
        """Display masked card number for security"""
        if obj.card_number:
            return f"{'*' * 12}{obj.card_number[-4:]}"
        return "-"
    
    card_number_masked.short_description = 'Card Number'
