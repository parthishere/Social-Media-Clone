# Generated by Django 3.2.4 on 2021-07-17 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(default='Cool✨'),
        ),
    ]