from django.urls import path
from .views import EmployeeAPIView

urlpatterns = [
    path('employee', EmployeeAPIView.as_view()),
]