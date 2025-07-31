from django.contrib import admin
from .models import (
    Subscription,
    Plan,
    ExchangeRateLog
)

class ExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ("id", "currency_pair", "rate", "fetched_at")
    list_filter = ("base_currency", "target_currency", "fetched_at")
    search_fields = ("base_currency", "target_currency")
    date_hierarchy = "fetched_at"
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20

    def currency_pair(self, obj):
        return f"{obj.base_currency} → {obj.target_currency}"
    currency_pair.short_description = "Currency Pair"

admin.site.register(Subscription)
admin.site.register(Plan)
admin.site.register(ExchangeRateLog, ExchangeRateLogAdmin)
