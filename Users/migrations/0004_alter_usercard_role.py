# Generated by Django 4.2.2 on 2023-06-19 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_remove_usercard_first_name_remove_usercard_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercard',
            name='role',
            field=models.CharField(choices=[('T', 'Teacher'), ('A', 'Alumnus/Alumna'), ('W', 'Worker'), ('S', 'Student'), ('O', 'Office Member')], max_length=10),
        ),
    ]
