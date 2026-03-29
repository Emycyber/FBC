from django.db import models
from wagtail.models import Page



class BettingCompany(models.Model):
    # A separate model to store each betting company
    # This allows each company to have a name AND a logo

    name = models.CharField(max_length=100)
    # The company name e.g "Sportybet", "Bet9ja"

    logo = models.ImageField(
        upload_to='company_logos/',
        # upload_to: folder inside MEDIA_ROOT where logos are saved
        # uploaded logos go to media/company_logos/
        null=True,
        blank=True,
        # null=True blank=True: logo is optional
        # company can exist without a logo
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Betting Companies'
        # Fixes admin label from "Betting Companys" to "Betting Companies"

    def __str__(self):
        return self.name
        # Shows company name in admin dropdown when selecting a company


class BookingCode(models.Model):
    date = models.DateField()

    company = models.ForeignKey(
        BettingCompany,
        # ForeignKey links each booking code to a BettingCompany object
        # instead of typing the company name as text
        # you now SELECT a company from a dropdown in admin
        on_delete=models.CASCADE,
        # CASCADE: if a company is deleted, all its booking codes are deleted too
        null=True,
        blank=True,
    )

    booking_code = models.CharField(max_length=200)

    accumulated_odds = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.company} - {self.booking_code} ({self.date})"
    
    class HomePage(Page):
    # Simple home page model
    # Wagtail needs this to have a proper page tree
    
        class Meta:
            verbose_name = 'Home Page'

        def get_context(self, request):
            context = super().get_context(request)
            return context


class FooterLink(models.Model):
    # Each FooterLink is one link shown in the footer
    
    title = models.CharField(max_length=200)
    # The link text e.g "Soccervista"
    
    url = models.URLField()
    # The actual URL e.g "https://soccervista.com"
    
    order = models.IntegerField(default=0)
    # Controls the order links appear in the footer
    # lower number = appears first
    
    is_active = models.BooleanField(default=True)
    # allows you to hide a link without deleting it
    
    class Meta:
        ordering = ['order']
        # shows links in order number sequence
        verbose_name = 'Footer Link'
        verbose_name_plural = 'Footer Links'
    
    def __str__(self):
        return self.title
    
    
    
class Partner(models.Model):
    name = models.CharField(max_length=200)
    # Partner website name e.g "Soccervista"

    url = models.URLField()
    # Partner website URL e.g "https://soccervista.com"


    order = models.IntegerField(
        default=0,
        help_text='Controls display order, lower number appears first'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Uncheck to hide partner without deleting'
    )

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return self.name
    
class VIPCode(models.Model):
    # Premium booking codes only for VIP subscribers
    # Separate from the free codes on homepage

    date = models.DateField()

    company = models.ForeignKey(
        BettingCompany,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    booking_code = models.CharField(max_length=200)

    accumulated_odds = models.DecimalField(max_digits=10, decimal_places=2)

    PLAN_CHOICES = [
        ('safe', 'Safe Odds (1.6 - 2.5)'),
        ('high', 'High Odds (2.0 - 3.0)'),
        ('both', 'Both Plans'),
        # both: visible to all VIP subscribers
    ]

    plan = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default='both',
        help_text='Which subscription plan can see this code'
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'VIP Code'
        verbose_name_plural = 'VIP Codes'

    def __str__(self):
        return f"{self.company} - {self.booking_code} ({self.date})"