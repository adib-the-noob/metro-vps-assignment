from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Plan, Subscription
from config.responses import APIResponse
from .serializers import PlanSerializer, SubcribePlanSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_all_plans(request):
    plans = Plan.objects.all()
    serializer = PlanSerializer(plans, many=True)
    return APIResponse(data=serializer.data, status=status.HTTP_200_OK, message="Plans retrieved successfully.")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def subscribe(request, plan_id):
    user = request.user
    serializer = SubcribePlanSerializer(data=request.data)
    if serializer.is_valid():
        subscription = Subscription.objects.create(
            user=user,
            plan_id=plan_id,
            status=serializer.validated_data['status'],
            end_date=serializer.validated_data['end_date']
        )
        subscription.save()
        return APIResponse(
            data={
                "status": "success",
            "message": "Subscribed successfully.",
            "data": {
                "subscription": {
                    "id": subscription.id,
                    "user": user.username,
                    "plan": subscription.plan.name,
                    "start_date": subscription.start_date,
                    "end_date": subscription.end_date
                }, 
                "plan": {
                    "id": subscription.plan.id,
                    "name": subscription.plan.name,
                    "price": subscription.plan.price
                }
            }
        }, status=status.HTTP_201_CREATED, message="Subscription created successfully.")