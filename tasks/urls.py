from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("addNotification/", views.CreateTaskView.as_view(), name="create notifiaction"),
    path("getalltasks/", views.GetTaskView.as_view(), name="get task")
]