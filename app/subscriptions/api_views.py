from django.utils import timezone
from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Plan, Subscription
from config.responses import APIResponse
from .serializers import (
    UserSubscriptionSerializer, 
    SubscriptionPlanIdSerializer,
    CancelSubscriptionSerializer
)

class UserSubscribeApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            subscriptions = Subscription.objects.filter(user=request.user, status="active").select_related('plan')
            serializer = UserSubscriptionSerializer(subscriptions, many=True)
            return APIResponse(
                data=serializer.data,   
                status=status.HTTP_200_OK,
                message="Subscriptions retrieved successfully."
            )
        except Exception as e:
            return APIResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e)
            )
        
    # Subscribe to a plan
    def post(self, request): 
        try:
            serializer = SubscriptionPlanIdSerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                return APIResponse(
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Invalid data provided."
                )
            
            with transaction.atomic():
                past_subscription = Subscription.objects.select_for_update().filter(
                    user=request.user, 
                    plan_id=serializer.validated_data['plan_id'],
                    status='active',
                    end_date__gt=timezone.now()
                ).first()

                if past_subscription:
                    serializer = UserSubscriptionSerializer(past_subscription)
                    return APIResponse(
                        data=serializer.data,
                        status=status.HTTP_400_BAD_REQUEST,
                        message="You are already subscribed to this plan and it is still active."
                    )   
                plan = Plan.objects.get(id=serializer.validated_data['plan_id'])
                new_subscription = Subscription.objects.create(
                    user=request.user,
                    plan_id=plan.id,
                    end_date=timezone.now() + timezone.timedelta(days=plan.duration_days)
                )
                
            serializer = UserSubscriptionSerializer(new_subscription)
            return APIResponse(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Subscription created successfully."
            )
        except Exception as e:
            return APIResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e)
            )
            

class CancelSubscriptionApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            serializer = CancelSubscriptionSerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                return APIResponse(
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Invalid data provided."
                )
            with transaction.atomic():
                # Use select_for_update to prevent race conditions
                subscription = Subscription.objects.select_for_update().filter(
                    user=request.user,
                    id=serializer.validated_data['subscription_id'],
                    status='active'
                ).first()
                
                if not subscription:
                    return APIResponse(
                        data=None,
                        status=status.HTTP_404_NOT_FOUND,
                        message="Subscription not found!"
                    )
                
                # Update subscription status
                subscription.end_date = timezone.now()
                subscription.status = 'cancelled'
                subscription.save()
            
            serializer = UserSubscriptionSerializer(subscription)
            return APIResponse(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Subscription cancelled successfully."
            )
            
        except Exception as e:
            return APIResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e)
            )