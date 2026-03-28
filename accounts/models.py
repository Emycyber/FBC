from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subscription(models.Model):

    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    PLAN_CHOICES = [
        (WEEKLY, 'Weekly - 7 Days'),
        (MONTHLY, 'Monthly - 30 Days'),
        # each tuple is (database_value, human_readable_label)
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='subscription'
        # OneToOneField: each user can only have one subscription
        # related_name: allows us to access subscription from user
        # e.g user.subscription
    )

    plan = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default=WEEKLY,
        # choices: shows dropdown in admin with plan options
    )

    is_active = models.BooleanField(
        default=False,
        # default False: subscription starts inactive
        # admin manually activates it after payment confirmation
    )

    start_date = models.DateTimeField(
        null=True,
        blank=True,
        # set when admin activates subscription
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
        # automatically calculated based on plan
    )

    created_at = models.DateTimeField(auto_now_add=True)
    # tracks when subscription was first created

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f"{self.user.username} - {self.plan} - {'Active' if self.is_active else 'Inactive'}"

    def is_valid(self):
        # checks if subscription is active AND not expired
        if self.is_active and self.end_date:
            return timezone.now() < self.end_date
            # timezone.now(): current date and time
            # returns True if current time is before end date
        return False

    def activate(self):
        # called when admin activates a subscription
        self.is_active = True
        self.start_date = timezone.now()

        if self.plan == self.WEEKLY:
            from datetime import timedelta
            self.end_date = timezone.now() + timedelta(days=7)
            # timedelta(days=7): adds 7 days to current time
        elif self.plan == self.MONTHLY:
            from datetime import timedelta
            self.end_date = timezone.now() + timedelta(days=30)
            # timedelta(days=30): adds 30 days to current time

        self.save()