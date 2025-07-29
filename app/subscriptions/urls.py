from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscriptions_list, name='subscriptions_list'),
]