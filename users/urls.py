from django.urls import path
from .views import (
    RegisterView,
    UserDetailView,
    CustomTokenObtainPairView,
    TelegramConnectView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('telegram/connect/', TelegramConnectView.as_view(), name='telegram-connect'),
]
