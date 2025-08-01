from django.utils import timezone
from .models import ExchangeRateLog
from utils.caller import compare_exchange_rate
from celery import shared_task


@shared_task
def fetch_exchange_rate():
    response = compare_exchange_rate('USD', 'BDT')
    if response:
        ExchangeRateLog.objects.create(
            base_currency=response['base_code'],
            target_currency=response['target_code'],
            fetched_at=timezone.now(),
            rate=response['conversion_rate']
        )
        print(f"Exchange rate '{response['base_code']}/{response['target_code']}' fetched and logged successfully.")
    return None