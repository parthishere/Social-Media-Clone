# Generated by Django 3.2.4 on 2021-06-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='caption',
            field=models.TextField(default='feeling good ✔🎶'),
        ),
    ]
