from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import BookingCode, BettingCompany, FooterLink, Partner, VIPCode, Prediction
 


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
    
    

@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'is_active']
    # shows all fields in admin list view
    list_editable = ['order', 'is_active']
    # list_editable: allows editing order and active status
    # directly from the list view without opening each link
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
    
    

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'league',
        'home_team',
        'away_team',
        'tip',
        'odds',
        'result',
        'is_vip'
    ]
    list_filter = ['result', 'is_vip', 'date', 'league']
    list_editable = ['result', 'is_vip']
    # list_editable: update result and vip status
    # directly from the list view
    search_fields = ['home_team', 'away_team', 'league']
    ordering = ['-date', 'match_time']
    
    

class APIFootballAdminLink(admin.ModelAdmin):
    pass

# Add custom link to admin index
admin.site.index_template = 'admin/custom_index.html'