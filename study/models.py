from django.db import models


class Student(models.Model):
    username = models.CharField(max_length=31, unique=True)
    password = models.CharField(max_length=256)
    fullname = models.CharField(max_length=254)
    email = models.CharField(max_length=254)
    birthday = models.DateField()
    level = models.IntegerField()
    image_id = models.IntegerField()


class Teacher(models.Model):
    username = models.CharField(max_length=31, unique=True)
    password = models.CharField(max_length=256)
    fullname = models.CharField(max_length=254)
    email = models.CharField(max_length=254)
    birthday = models.DateField()
    account = models.CharField(max_length=254)


class Category(models.Model):
    name = models.CharField(max_length=64)


class Content(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    content = models.TextField()
    level = models.IntegerField()


class Curriculum(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    content = models.ForeignKey('Content', on_delete=models.CASCADE)
    percentage = models.IntegerField()
    score = models.IntegerField(null=True)


class DownloadHistory(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    content = models.ForeignKey('Content', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)