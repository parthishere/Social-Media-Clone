# Generated by Django 3.2.4 on 2021-06-26 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20210626_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='content',
            field=models.TextField(default='You have notification', max_length=255),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=10),
        ),
    ]
