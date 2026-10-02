from django.urls import path
from .views import MeView, StatusView, AccessTokenLoginView, RefreshTokenView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('status/', StatusView.as_view(), name='status'),
    path('login/', AccessTokenLoginView.as_view(), name='access-token-login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh-token')
]
