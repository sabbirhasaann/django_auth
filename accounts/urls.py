from django.urls import path
from .views import MeView, StatusView, AccessTokenLoginView, RefreshTokenView, LoginView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('status/', StatusView.as_view(), name='status'),
    path('login/', AccessTokenLoginView.as_view(), name='access-token-login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('v2/login/', LoginView.as_view(), name='v2-login'),
]
