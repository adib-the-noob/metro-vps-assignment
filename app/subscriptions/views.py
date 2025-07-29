from django.shortcuts import render
from .models import (
    Plan,
    Subscription,
    User
)

def subscriptions_list(request):
    subscriptions = Subscription.objects.select_related('user', 'plan').all()
    plans = Plan.objects.all()
    context = {
        'total_users': User.objects.count(),
        'subscriptions': subscriptions,
        'active_subscriptions': subscriptions.filter(status='active').count(),
        'plans': plans,
        'total_plans': plans.count(),
    }
    return render(request, 'dashboard.html', context)
