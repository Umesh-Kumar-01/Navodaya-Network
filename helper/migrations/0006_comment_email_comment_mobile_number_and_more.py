# Generated by Django 4.2.2 on 2023-07-19 13:27

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0005_rename_deletion_date_request_deletion_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=django_cryptography.fields.encrypt(models.EmailField(blank=True, max_length=254, null=True)),
        ),
        migrations.AddField(
            model_name='comment',
            name='mobile_number',
            field=django_cryptography.fields.encrypt(models.IntegerField(blank=True, null=True)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=django_cryptography.fields.encrypt(models.TextField()),
        ),
    ]
