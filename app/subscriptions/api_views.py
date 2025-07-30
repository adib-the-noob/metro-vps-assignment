from django.utils import timezone
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
                data=None,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )
        
    # Subscribe to a plan
    def post(self, request): 
        serializer = SubscriptionPlanIdSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            past_subscription = Subscription.objects.filter(
                user=request.user, 
                plan_id=serializer.validated_data['plan_id']
            ).first()
            if past_subscription and past_subscription.end_date > timezone.now():
                return APIResponse(
                    data=UserSubscriptionSerializer(past_subscription).data,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="You are already subscribed to this plan and it is still active."
                )
            plan = Plan.objects.get(id=serializer.validated_data['plan_id'])
            new_subscription = Subscription.objects.create(
                user=request.user,
                plan_id=serializer.validated_data['plan_id'],
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=plan.duration_days)
            )
            return APIResponse(
                data=UserSubscriptionSerializer(new_subscription).data,
                status=status.HTTP_200_OK,
                message="Subscription created successfully."
            )
        return APIResponse(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            message="Invalid data provided."
        )   
    

class CancelSubscriptionApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = SubscriptionPlanIdSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            subscription = Subscription.objects.filter(
                user=request.user, 
                plan_id=serializer.validated_data['plan_id']
            ).first()
            if not subscription:
                return APIResponse(
                    data=None,
                    status=status.HTTP_404_NOT_FOUND,
                    message="Subscription not found."
                )
            subscription.delete()
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