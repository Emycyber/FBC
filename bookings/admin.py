from django.contrib import admin
from django.utils.html import format_html
from .models import BookingCode, BettingCompany, FooterLink, Partner, VIPCode, DirectWinPrediction


@admin.register(BettingCompany)
class BettingCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" height="40" style="object-fit:contain;"/>',
                obj.logo.url
            )
        return 'No logo'
    logo_preview.short_description = 'Logo'


@admin.register(BookingCode)
class BookingCodeAdmin(admin.ModelAdmin):
    list_display = ['date', 'company', 'booking_code', 'accumulated_odds']
    list_filter = ['company', 'date']
    search_fields = ['company__name', 'booking_code']
    ordering = ['-date']


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(VIPCode)
class VIPCodeAdmin(admin.ModelAdmin):
    list_display = ['date', 'company', 'booking_code', 'accumulated_odds', 'result']
    list_filter = ['result', 'date', 'company']
    list_editable = ['result']
    search_fields = ['company__name', 'booking_code']
    ordering = ['-date']


@admin.register(DirectWinPrediction)
class DirectWinPredictionAdmin(admin.ModelAdmin):
    list_display = ['date', 'match', 'tip']
    fields = ['date', 'match', 'tip']
    list_filter = ['date']
    search_fields = ['match', 'tip']
    ordering = ['-date']