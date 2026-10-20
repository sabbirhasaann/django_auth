from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import (
    ProjectSerializer,
    ProjectCreateSerializer
)

# GET /api/projects/tasks/87/


class TaskAPIView(APIView):

    def get(self, request):
        pass


# POST /api/projects/project/create/

class CreateProjectAPIView(APIView):

    permission_class = [IsAuthenticated]

    @extend_schema(
        summary="Create a project",
        description="Creates a new product.",
        request=ProjectCreateSerializer,
        responses=ProjectSerializer,
    )
    
    def post(self, request):

        serializer = ProjectCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        project = serializer.save()

        response_project = ProjectSerializer(project)

        return Response(
            response_project.data,
            status=status.HTTP_201_CREATED,
        )
