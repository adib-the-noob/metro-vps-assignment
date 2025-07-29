from django.contrib import admin
from .models import (
    Subscription,
    Plan,
    ExchangeRateLog
)

admin.site.register(Subscription)
admin.site.register(Plan)
admin.site.register(ExchangeRateLog)
