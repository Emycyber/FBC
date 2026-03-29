from django.contrib import admin
from django.utils import timezone
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'plan',
        'is_active',
        'start_date',
        'end_date',
    ]
    # removed status_badge and days_remaining completely
    # they were causing the format_html error
    # the is_active, start_date and end_date columns
    # give you all the information you need

    list_filter = ['plan', 'is_active']
    search_fields = ['user__username', 'user__email']
    list_editable = ['is_active']
    # list_editable: lets you toggle is_active directly
    # from the list view without opening each subscription
    actions = ['activate_subscriptions', 'deactivate_subscriptions']

    def activate_subscriptions(self, request, queryset):
        for subscription in queryset:
            subscription.activate()
        self.message_user(
            request,
            f"{queryset.count()} subscription(s) activated successfully!"
        )
    activate_subscriptions.short_description = 'Activate selected subscriptions'

    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(
            request,
            f"{queryset.count()} subscription(s) deactivated!"
        )
    deactivate_subscriptions.short_description = 'Deactivate selected subscriptions'