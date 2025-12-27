from django.urls import path
from .views import *

urlpatterns = [
    path("", today_tasks),
    path("upcoming/", upcoming_tasks),
    path("completed/", completed_tasks),

    path("add/", add_task),
    path("task/<int:task_id>/", task_detail),
    path("delete/<int:task_id>/", delete_task),

    path("api/tasks/", task_api),
    path("api/tasks/<int:task_id>/", task_api),
]
