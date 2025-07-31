from django.urls import path
from . import views
from .api_views import (
    UserSubscribeApiView,
    CancelSubscriptionApiView
)
from .exchange_api_views import (
    get_exchange_rates,
    compare_exchange
)

urlpatterns = [
    path('', views.subscriptions_list, name='subscriptions_list'),
    
    # apis
    path('api/subscriptions/', UserSubscribeApiView.as_view(), name='get_all_plans'),
    path('api/subscribe/', UserSubscribeApiView.as_view(), name='subscribe'),
    path('api/cancel-subscription/', CancelSubscriptionApiView.as_view(), name='cancel_subscription'),

    # exchange rate APIs
    path('api/exchange-rates/<str:base_currency>/<str:target_currency>/', get_exchange_rates, name='get_exchange_rates'),
    path('api/compare-exchange', compare_exchange, name='compare_exchange'),
]