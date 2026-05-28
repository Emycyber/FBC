from django.db import models
from wagtail.models import Page


class BettingCompany(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to='company_logos/',
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text='URL friendly name e.g sportybet-booking-codes'
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Betting Companies'

    def __str__(self):
        return self.name


class BookingCode(models.Model):
    date = models.DateField()
    company = models.ForeignKey(
        BettingCompany,
        on_delete=models.CASCADE,
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

    class Meta:
        verbose_name = 'Home Page'

    content_panels = Page.content_panels

    def get_context(self, request):
        context = super().get_context(request)
        return context


class FooterLink(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Footer Link'
        verbose_name_plural = 'Footer Links'

    def __str__(self):
        return self.title


class Partner(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    logo = models.ImageField(
        upload_to='partner_logos/',
        null=True,
        blank=True,
        help_text='Optional partner logo image'
    )
    description = models.TextField(
        blank=True,
        help_text='Short description of the partner site'
    )
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
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'VIP Code'
        verbose_name_plural = 'VIP Codes'

    def __str__(self):
        return f"{self.company} - {self.booking_code} ({self.date})"


class DirectWinPrediction(models.Model):
    date = models.DateField()
    match = models.CharField(
        max_length=200,
        help_text='e.g Arsenal vs Chelsea'
    )
    tip = models.CharField(
        max_length=200,
        help_text='e.g Home Win, Over 2.5, BTTS'
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Direct Win Prediction'
        verbose_name_plural = 'Direct Win Predictions'

    def __str__(self):
        return f"{self.match} - {self.tip} ({self.date})"