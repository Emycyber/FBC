from django.db import models


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