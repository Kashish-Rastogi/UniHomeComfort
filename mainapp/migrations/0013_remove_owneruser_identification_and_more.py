# Generated by Django 5.0.1 on 2024-03-18 09:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_alter_category_description_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='city',
            field=models.TextField(default='Windsor', max_length=50),
        ),
        migrations.AddField(
            model_name='property',
            name='zipcode',
            field=models.TextField(default='N9B 2T6', max_length=50),
        ),

    ]
