# Generated by Django 3.1.6 on 2021-02-18 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=31, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('fullname', models.CharField(max_length=254)),
                ('email', models.CharField(max_length=254)),
                ('birthday', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=31, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('fullname', models.CharField(max_length=254)),
                ('email', models.CharField(max_length=254)),
                ('birthday', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.teacher')),
            ],
        ),
    ]
