from django.urls import path
from .views import (
    TaskAPIView,
    CreateProjectAPIView
)

urlpatterns = [
    path('tasks/<int:id>/', TaskAPIView.as_view(), name='task-by-id'),
    path('project/create/', CreateProjectAPIView.as_view(), name='create-project'),
]
