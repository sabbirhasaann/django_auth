from rest_framework import serializers

from .models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ProjectCreateSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True)

    def validate(self, attrs):
        print("attrs:...", attrs)
        return attrs

    def create(self, validated_data):

        print("validated-data...", validated_data)

        return Project.objects.create(**validated_data)
