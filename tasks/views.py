from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from task_manager.responseMessage import *
from .models import Task
import time
from .validations.task import (
    CreateTaskValidator,
    UpdateTaskValidator,
    DeleteTaskValidator,
)
from rest_framework.permissions import IsAuthenticated


class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = CreateTaskValidator(data=request.data)
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_FAILED,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Extract only required fields from request.data
            data = {
                "userId": request.user.id,
                "title": request.data.get("title"),
                "description": request.data.get("description"),
                "dueDate": request.data.get("dueDate"),
                "priority": request.data.get("priority"),
                "status": request.data.get("status"),
                "createdBy": str(request.user.id),
            }

            serializer = TaskSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": TASK_CREATED,
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": VALIDATION_FAILED,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            statusFilter = request.query_params.get("statusFilter", "").lower()

            # Base queryset: only tasks of this user
            tasks = Task.objects.filter(userId=user, isDeleted=False)

            # Apply status filter only if a valid status is provided
            if statusFilter:
                tasks = tasks.filter(status=statusFilter)

            # Apply status filter if not "all"
            if statusFilter:
                tasks = tasks.filter(status=statusFilter)

            taskData = list(
                tasks.order_by("-createdAt").values(
                    "id",
                    "title",
                    "userId",
                    "description",
                    "dueDate",
                    "priority",
                    "status",
                    "createdAt",
                )
            )

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": TASK_FETCH_SUCCESS,
                    "data": {
                        "count": tasks.count(),
                        "tasks": taskData,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, partial=True):
        try:
            user = request.user

            validator = UpdateTaskValidator(data=request.data, context={"user": user})
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_FAILED,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            task_id = request.data.get("id")

            # Ensure we only fetch a task that belongs to the authenticated user and is not deleted
            task = Task.objects.get(id=task_id, userId=user, isDeleted=False)
            if not task:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": TASK_NOT_FOUND,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = {}

            if "title" in request.data:
                data["title"] = request.data["title"]

            if "description" in request.data:
                data["description"] = request.data["description"]

            if "dueDate" in request.data:
                data["dueDate"] = request.data["dueDate"]

            if "priority" in request.data:
                data["priority"] = request.data["priority"]

            if "status" in request.data:
                data["status"] = request.data["status"]

            # always update metadata
            data["updatedBy"] = str(user.id)
            data["updatedAt"] = int(time.time() * 1000)

            serializer = TaskSerializer(task, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": TASK_UPDATED,
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": VALIDATION_FAILED,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user

            validator = DeleteTaskValidator(data=request.data, context={"user": user})
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_FAILED,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            task_id = request.data.get("id")

            # Ensure we only fetch a task that belongs to the authenticated user and is not deleted
            task = Task.objects.get(id=task_id, userId=user, isDeleted=False)

            # Soft delete: set isDeleted to True and update timestamps
            task.isDeleted = True
            task.updatedBy = str(user.id)
            task.updatedAt = int(time.time() * 1000)
            task.save()

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": TASK_DELETED,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CompleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user

            # Reuse DeleteTaskValidator which validates task id belongs to user and is not deleted
            validator = DeleteTaskValidator(data=request.data, context={"user": user})
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_FAILED,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            task_id = request.data.get("id")

            # Fetch the task (validator already ensured existence)
            task = Task.objects.get(id=task_id, userId=user, isDeleted=False)

            # Mark as completed
            task.status = "completed"
            task.updatedBy = str(user.id)
            task.updatedAt = int(time.time() * 1000)
            task.save()

            serializer = TaskSerializer(task)

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": TASK_UPDATED,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
