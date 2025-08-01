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
def compare_exchange(request):
    base_currency = request.query_params.get('base_currency')
    target_currency = request.query_params.get('target_currency')
    
    if not base_currency or not target_currency:
        return APIResponse(
            status=status.HTTP_400_BAD_REQUEST,
            message="Base currency and target currency are required."
        )

    rate = compare_exchange_rate(base_currency, target_currency)
    if rate is None:
        return APIResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Exchange rate not found."
        )
    ExchangeRateLog.objects.create(
        base_currency=rate['base_code'],
        target_currency=rate['target_code'],
        rate=rate['conversion_rate'],
    )
    return APIResponse(
        status=status.HTTP_200_OK,
        data=rate
    )
