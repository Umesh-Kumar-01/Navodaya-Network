# Generated by Django 4.2.2 on 2023-07-20 12:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_alter_usercard_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercard',
            name='profile_photo',
            field=models.ImageField(default='default_profile.png', upload_to='profile_photos/', validators=[django.core.validators.MaxLengthValidator(limit_value=102400, message='The image size should be less than 100KB.'), django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'], message='Only PNG and JPG files are allowed.')]),
        ),
    ]
