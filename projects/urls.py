from django.urls import path
from .views import (
    TaskAPIView,
    CreateProjectAPIView,
    TaskViewSet
)
from rest_framework.routers import SimpleRouter


urlpatterns = [
    path('tasks/<int:id>/', TaskAPIView.as_view(), name='task-by-id'),
    path('project/create/', CreateProjectAPIView.as_view(), name='create-project'),
    path('tasks/<int:pk>/retrieve/', TaskViewSet.as_view({
        'get': 'retrieve'
    }), name="task-retrieve"),
    path('tasks/', TaskViewSet.as_view({
        'get': 'list'
    })),
]
