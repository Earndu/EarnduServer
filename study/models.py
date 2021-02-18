from django.db import models

# Create your models here.
class Student(models.Model):
    username = models.CharField(max_length=31, unique=True)
    password = models.CharField(max_length=256)
    fullname = models.CharField(max_length=254)
    email = models.CharField(max_length=254)
    birthday = models.DateField()

class Teacher(models.Model):
    username = models.CharField(max_length=31, unique=True)
    password = models.CharField(max_length=256)
    fullname = models.CharField(max_length=254)
    email = models.CharField(max_length=254)
    birthday = models.DateField()

class Content(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    content = models.TextField()
