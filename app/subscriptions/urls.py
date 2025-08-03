from django.urls import path
from . import views
from .api_views import (
    UserSubscribeApiView,
    CancelSubscriptionApiView
)
from .exchange_api_views import (
    compare_exchange
)

urlpatterns = [
    path('', views.subscriptions_list, name='subscriptions_list'),
    
    # apis
    path('api/subscriptions/', UserSubscribeApiView.as_view(), name='get_all_plans'),
    path('api/subscribe/', UserSubscribeApiView.as_view(), name='subscribe'),
    path('api/cancel-subscription/', CancelSubscriptionApiView.as_view(), name='cancel_subscription'),

    # exchange rate APIs
    path('api/exchange-rate/', compare_exchange, name='compare_exchange'),
]