# Generated by Django 3.1.6 on 2021-03-02 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_auto_20210224_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculum',
            name='end_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.DeleteModel(
            name='DownloadHistory',
        ),
    ]