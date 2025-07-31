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
    SubscriptionPlanIdSerializer
)

class UserSubscribeApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            subscriptions = Subscription.objects.filter(user=request.user).select_related('plan')
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
            if serializer.is_valid():
                past_subscription = Subscription.objects.filter(
                    user=request.user, 
                    plan_id=serializer.validated_data['plan_id'],
                    status='active',
                    end_date__gt=timezone.now() # Check if the subscription is still active
                ).first()
                if past_subscription:
                    serializer = UserSubscriptionSerializer(past_subscription)
                    return APIResponse(
                        data=serializer.data,
                        status=status.HTTP_400_BAD_REQUEST,
                        message="You are already subscribed to this plan and it is still active."
                    )
                # Create a new subscription
                with transaction.atomic():
                    try:
                        plan = Plan.objects.get(id=serializer.validated_data['plan_id'])
                        new_subscription = Subscription.objects.create(
                            user=request.user,
                            plan_id=plan.id,
                            end_date=timezone.now() + timezone.timedelta(days=plan.duration_days)
                        )
                    except Exception as e:
                        return APIResponse(
                            data=None,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            message="Database error",
                            error=str(e)
                        )
                serializer = UserSubscriptionSerializer(new_subscription)
                return APIResponse(
                    data=serializer.data,
                    status=status.HTTP_200_OK,
                    message="Subscription created successfully."
                )
            return APIResponse(
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                message="Invalid data provided."
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
            serializer = SubscriptionPlanIdSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                subscription = Subscription.objects.filter(
                    user=request.user, 
                    plan_id=serializer.validated_data['plan_id'],
                    status='active',
                    end_date__gt=timezone.now()  # Ensure the subscription is still active
                ).first()
                if not subscription:
                    return APIResponse(
                        data=None,
                        status=status.HTTP_404_NOT_FOUND,
                        message="Subscription not found."
                    )
                subscription.status = 'cancelled'
                subscription.save()
        
                return APIResponse(
                    data=None,
                    status=status.HTTP_204_NO_CONTENT,
                    message="Subscription cancelled successfully."
                )
            return APIResponse(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                message="Invalid data provided."
            )
        except Exception as e:
            return APIResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e)
            )