from rest_framework import serializers
from task_manager.responseMessage import *
from ..models import Task
from task_manager.constants import PRIORITY_CHOICES, STATUS_CHOICES


# Validator classes (follow pattern from RegisterValidator / LoginValidator)
class CreateTaskValidator(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    dueDate = serializers.IntegerField(required=True)
    priority = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_priority(self, value):
        if value is not None and value not in PRIORITY_CHOICES:
            raise serializers.ValidationError(INVALID_PRIORITY)
        return value

    def validate_status(self, value):
        if value is not None and value not in STATUS_CHOICES:
            raise serializers.ValidationError(INVALID_STATUS)
        return value


class UpdateTaskValidator(serializers.Serializer):
    id = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    dueDate = serializers.IntegerField(required=False)
    priority = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_priority(self, value):
        if value is not None and value not in PRIORITY_CHOICES:
            raise serializers.ValidationError(INVALID_PRIORITY)
        return value

    def validate_status(self, value):
        if value is not None and value not in STATUS_CHOICES:
            raise serializers.ValidationError(INVALID_STATUS)
        return value


class DeleteTaskValidator(serializers.Serializer):
    id = serializers.CharField(required=True)

    def validate_id(self, value):
        user = self.context.get("user")
        if not Task.objects.filter(id=value, userId=user, isDeleted=False).exists():
            raise serializers.ValidationError(TASK_NOT_FOUND)
        return value
