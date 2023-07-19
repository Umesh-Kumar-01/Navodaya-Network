# Generated by Django 4.2.2 on 2023-07-19 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0006_comment_email_comment_mobile_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='mobile_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
    ]
