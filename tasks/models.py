from django.db import models
import time
from users.models import User
from task_manager.constants import PRIORITY_CHOICES, STATUS_CHOICES
import uuid


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, db_column="userId"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=True)
    dueDate = models.BigIntegerField()
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Unix timestamp fields
    createdAt = models.BigIntegerField(default=int(time.time() * 1000))
    updatedAt = models.BigIntegerField(default=int(time.time() * 1000))

    # User fields
    createdBy = models.CharField(
        null=True,
        blank=False,
    )
    updatedBy = models.CharField(
        null=True,
        blank=False,
    )
    isDeleted = models.BooleanField(default=False)

    class Meta:
        db_table = "task"
