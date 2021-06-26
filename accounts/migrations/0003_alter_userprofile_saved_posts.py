# Generated by Django 3.2.4 on 2021-06-26 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_caption'),
        ('accounts', '0002_alter_userprofile_saved_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='saved_posts',
            field=models.ManyToManyField(blank=True, to='post.Post'),
        ),
    ]