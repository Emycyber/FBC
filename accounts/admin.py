from django.contrib import admin
from django.utils.html import format_html
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
        'status_badge',
        'days_remaining'
    ]
    list_filter = ['plan', 'is_active']
    search_fields = ['user__username', 'user__email']
    actions = ['activate_subscriptions', 'deactivate_subscriptions']

    def status_badge(self, obj):
        if obj.is_valid():
            return format_html(
                '<span style="background:#198754; color:white; '
                'padding:3px 10px; border-radius:20px; '
                'font-size:0.8rem;">✅ Active</span>'
            )
            # format_html with no extra arguments - just a plain string
        return format_html(
            '<span style="background:#dc3545; color:white; '
            'padding:3px 10px; border-radius:20px; '
            'font-size:0.8rem;">❌ Expired</span>'
        )
    status_badge.short_description = 'Status'

    def days_remaining(self, obj):
        if obj.is_valid():
            remaining = obj.end_date - timezone.now()
            days = remaining.days
            return format_html(
                '<span style="color:#198754; font-weight:600;">{} days left</span>',
                days
                # passing days as a separate argument to format_html
                # this is the correct way to include variables
            )
        return format_html(
            '<span style="color:#dc3545; font-weight:600;">Expired</span>'
        )
    days_remaining.short_description = 'Days Remaining'

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