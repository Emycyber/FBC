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
    template = 'blog/home_page.html'

    subpage_types = ['blog.BlogIndexPage']
    # only BlogIndexPage can be created under HomePage

    class Meta:
        verbose_name = 'Home Page'

    content_panels = Page.content_panels

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
    date = models.DateField()

    company = models.ForeignKey(
        BettingCompany,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    booking_code = models.CharField(max_length=200)
    accumulated_odds = models.DecimalField(max_digits=10, decimal_places=2)

    # Result choices
    PENDING = 'pending'
    WON = 'won'
    LOST = 'lost'

    RESULT_CHOICES = [
        (PENDING, 'Pending'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    ]

    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES,
        default=PENDING,
        # starts as pending, admin updates after game
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'VIP Code'
        verbose_name_plural = 'VIP Codes'

    def __str__(self):
        return f"{self.company} - {self.booking_code} ({self.date})"
    
    
class Prediction(models.Model):

    # Result choices
    PENDING = 'pending'
    WON = 'won'
    LOST = 'lost'

    RESULT_CHOICES = [
        (PENDING, 'Pending'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    ]

    date = models.DateField()
    # match date

    league = models.CharField(max_length=100)
    # e.g "Premier League", "La Liga"

    league_logo = models.URLField(blank=True)
    # URL of league logo from API Football

    home_team = models.CharField(max_length=100)
    # home team name

    home_team_logo = models.URLField(blank=True)
    # URL of home team logo from API Football

    away_team = models.CharField(max_length=100)
    # away team name

    away_team_logo = models.URLField(blank=True)
    # URL of away team logo from API Football

    match_time = models.TimeField()
    # kick off time

    tip = models.CharField(
        max_length=100,
        help_text='e.g Over 1.5, Home Win, BTTS, X2'
    )
    # the prediction tip

    odds = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Odds for this prediction'
    )

    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES,
        default=PENDING,
    )

    is_vip = models.BooleanField(
        default=False,
        help_text='Check to show only on VIP page'
    )
    # is_vip: if True only VIP subscribers can see it
    # if False shows on free predictions page

    class Meta:
        ordering = ['-date', 'match_time']
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.tip} ({self.date})"    