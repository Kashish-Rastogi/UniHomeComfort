# Generated by Django 5.0.1 on 2024-03-10 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_property_allowed_lease_people_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], default='Female', max_length=7),
        ),
    ]
