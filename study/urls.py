from django.urls import path
from . import views

urlpatterns = [
    path('teacher', views.teacher_many),
    path('teacher/<int:teacher_id>', views.teacher_one),
    path('teacher/login', views.teacher_login),
]