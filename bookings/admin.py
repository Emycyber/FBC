from django.contrib import admin
from django.utils.html import format_html
from .models import BookingCode, BettingCompany

# Register your models here.

@admin.register(BettingCompany)
class BettingCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" height="40" style="object-fit:contain;"/>',
                obj.logo.url
                # shows a small logo preview in the admin list
            )
        return 'No logo'
    logo_preview.short_description = 'Logo'



@admin.register(BookingCode)
class BookingCodeAdmin(admin.ModelAdmin):
    list_display = ['date', 'company', 'booking_code', 'accumulated_odds']
    list_filter = ['company', 'date']
    search_fields = ['company__name', 'booking_code']
    # company__name: searches through the related BettingCompany name
    ordering = ['-date']