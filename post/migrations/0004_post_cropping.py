# Generated by Django 3.2.4 on 2021-07-15 14:19

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20210715_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '430x360', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
    ]
