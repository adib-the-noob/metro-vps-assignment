from django.urls import path
from .views import (
    RegistrationView, 
    LoginView,
    UserProfileView

)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]