from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(help_text="Duration in days")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price} for {self.duration_days} days"


class Subscription(models.Model):
    SUBSCRIPTION_STATUS = (
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="subscriptions")

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=SUBSCRIPTION_STATUS, default="active")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]
        unique_together = ("user", "plan", "start_date")

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} subscription"

    @property
    def is_active(self):
        return self.status == "active" and timezone.now() < self.end_date


class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=10)
    target_currency = models.CharField(max_length=10)
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    date = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Exchange rate from {self.base_currency} to {self.target_currency} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}: {self.rate}"
