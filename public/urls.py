from django.urls import path
from .views import PublicView

urlpatterns = [
    path('', PublicView.as_view(), name='public-view')
]
