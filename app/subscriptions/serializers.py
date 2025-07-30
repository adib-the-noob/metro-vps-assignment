from rest_framework import serializers
from .models import Plan, Subscription
from django.utils import timezone

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'id',
            'name',
            'price',
            'duration_days',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'start_date',
            'end_date',
            'status',
            'created_at',
            'updated_at',
            'plan',
        ]
        read_only_fields = ['start_date', 'created_at', 'updated_at']


class SubscriptionPlanIdSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()

    def validate(self, data):
        plan_id = data.get('plan_id')
        if not Plan.objects.filter(id=plan_id).exists():
            raise serializers.ValidationError("Plan with this ID does not exist.")
        return data
    