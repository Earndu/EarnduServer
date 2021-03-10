from django.urls import path
from . import views

urlpatterns = [
    path('teacher', views.teacher_many),
    path('teacher/<int:teacher_id>', views.teacher_one),
    path('teacher/login', views.teacher_login),
    path('student', views.student_many),
    path('student/login', views.student_login),
    path('category', views.category_many),
    path('content', views.content_many),
    path('content/<int:content_id>', views.content_one),
    path('logout', views.logout),
    path('curriculum', views.curriculum_many),
]