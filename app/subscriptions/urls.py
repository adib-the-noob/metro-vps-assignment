from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.subscriptions_list, name='subscriptions_list'),
    # apis
    path('api/plans/', api_views.get_all_plans, name='get_all_plans'),
    path('api/subscribe/<int:plan_id>/', api_views.subscribe, name='subscribe'),
]