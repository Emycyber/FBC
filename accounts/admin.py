from django.contrib import admin
from django.utils.html import format_html
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
    # user__username: searches through related User model
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    # actions: bulk actions available in admin list view

    def status_badge(self, obj):
        if obj.is_valid():
            return format_html(
                '<span style="background:#198754; color:white; '
                'padding:3px 10px; border-radius:20px; font-size:0.8rem;">'
                '✅ Active</span>'
            )
        return format_html(
            '<span style="background:#dc3545; color:white; '
            'padding:3px 10px; border-radius:20px; font-size:0.8rem;">'
            '❌ Expired</span>'
        )
    status_badge.short_description = 'Status'

    def days_remaining(self, obj):
        if obj.is_valid():
            from django.utils import timezone
            remaining = obj.end_date - timezone.now()
            return f"{remaining.days} days left"
        return 'Expired'
    days_remaining.short_description = 'Days Remaining'

    def activate_subscriptions(self, request, queryset):
        for subscription in queryset:
            subscription.activate()
        self.message_user(request, f"{queryset.count()} subscription(s) activated!")
    activate_subscriptions.short_description = 'Activate selected subscriptions'

    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} subscription(s) deactivated!")
    deactivate_subscriptions.short_description = 'Deactivate selected subscriptions'