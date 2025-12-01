from django.urls import path
from .views import (
    CreateTaskView,
    TaskListView,
    UpdateTaskView,
    DeleteTaskView,
    CompleteTaskView,
)

app_name = "tasks"

urlpatterns = [
    path("create-task/", CreateTaskView.as_view(), name="createTask"),
    path("all-task/", TaskListView.as_view(), name="allTasks"),
    path("update-task/<uuid:pk>/", UpdateTaskView.as_view(), name="updateTask"),
    path("delete-task/", DeleteTaskView.as_view(), name="delete-task"),
    path("complete-task/", CompleteTaskView.as_view(), name="complete-task"),
]
