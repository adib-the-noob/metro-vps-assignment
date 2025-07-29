from rest_framework import serializers
from .models import Plan, Subscription

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubcribePlanSerializer(serializers.Serializer):
    CHOICES = (
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
    )
    status = serializers.ChoiceField(choices=CHOICES)
    end_date = serializers.DateTimeField()
