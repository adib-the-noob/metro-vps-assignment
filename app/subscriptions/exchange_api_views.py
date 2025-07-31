from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.responses import APIResponse
from .models import ExchangeRateLog
from utils.caller import compare_exchange_rate


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_exchange_rates(request, base_currency, target_currency):
    try:
        exchange_rate_log = ExchangeRateLog.objects.filter(
            base_currency=base_currency,
            target_currency=target_currency
        ).order_by('-date').first()

        if not exchange_rate_log:
            return APIResponse(
                status=status.HTTP_404_NOT_FOUND,
                message="Exchange rate not found."
            )

        data = {
            'base_currency': exchange_rate_log.base_currency,
            'target_currency': exchange_rate_log.target_currency,
            'rate': str(exchange_rate_log.rate),
            'date': exchange_rate_log.date.strftime('%Y-%m-%d %H:%M:%S')
        }

        return APIResponse(
            status=status.HTTP_200_OK,
            data=data
        )

    except Exception as e:
        return APIResponse(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def compare_exchange(request):
    base_currency = request.query_params.get('base_currency')
    target_currency = request.query_params.get('target_currency')
    amount = float(request.query_params.get('amount', 1.0))
    
    if not base_currency or not target_currency:
        return APIResponse(
            status=status.HTTP_400_BAD_REQUEST,
            message="Base currency and target currency are required."
        )

    rate = compare_exchange_rate(base_currency, target_currency, amount)
    if rate is None:
        return APIResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Exchange rate not found."
        )
    ExchangeRateLog.objects.create(
        base_currency=rate['base_code'],
        target_currency=rate['target_code'],
        rate=rate['conversion_rate'],
        # fetched_at=timezone.now()
    )
    return APIResponse(
        status=status.HTTP_200_OK,
        data=rate
    )
