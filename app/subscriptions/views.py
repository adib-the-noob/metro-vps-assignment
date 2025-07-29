from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render

from config.responses import APIResponse
from .models import (
    Plan,
    Subscription,
    User
)

def subscriptions_list(request):
    subscriptions = Subscription.objects.select_related('user', 'plan').all()
    context = {
        'subscriptions': subscriptions,
    }
    return render(request, 'dashboard.html', context)
