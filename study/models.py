from django.db import models


class Student(models.Model):
    username = models.CharField(max_length=31, unique=True)
    password = models.CharField(max_length=256)
    fullname = models.CharField(max_length=254)
    email = models.CharField(max_length=254)
    birthday = models.DateField()
    level = models.IntegerField(default=0)
    image_id = models.IntegerField()


class Teacher(models.Model):
    username = models.CharField(max_length=31, unique=True)
    password = models.CharField(max_length=256)
    fullname = models.CharField(max_length=254)
    email = models.CharField(max_length=254)
    birthday = models.DateField()
    account = models.CharField(max_length=254)


class Category(models.Model):
    english = models.CharField(max_length=64)


class Content(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    type = models.IntegerField()
    content = models.TextField()
    level = models.IntegerField()
    res_image = models.TextField(null=True)
    res_sound = models.TextField(null=True)


class Curriculum(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    content = models.ForeignKey('Content', on_delete=models.CASCADE)
    percentage = models.IntegerField()
    score = models.IntegerField(null=True)
    end_datetime = models.DateTimeField(null=True)


class Quiz(models.Model):
    content = models.ForeignKey('Content', on_delete=models.CASCADE)
    question = models.TextField()
    answer_1 = models.TextField()
    answer_2 = models.TextField()
    answer_3 = models.TextField()
    answer_4 = models.TextField()
    answer = models.IntegerField()
    res_image = models.TextField(null=True)
    res_sound = models.TextField(null=True)
    level = models.IntegerField()