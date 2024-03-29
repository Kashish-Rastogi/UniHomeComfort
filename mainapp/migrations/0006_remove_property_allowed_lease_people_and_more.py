# Generated by Django 5.0.1 on 2024-02-27 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_owneruser_occupation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='allowed_lease_people',
        ),
        migrations.RemoveField(
            model_name='property',
            name='house_build_date',
        ),
        migrations.RemoveField(
            model_name='property',
            name='lease_duration',
        ),
        migrations.RemoveField(
            model_name='property',
            name='lease_required',
        ),
        migrations.RemoveField(
            model_name='property',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='property',
            name='prop_image1',
        ),
        migrations.RemoveField(
            model_name='property',
            name='prop_image2',
        ),
        migrations.RemoveField(
            model_name='property',
            name='prop_image3',
        ),
        migrations.RemoveField(
            model_name='property',
            name='prop_image4',
        ),
        migrations.RemoveField(
            model_name='property',
            name='prop_image5',
        ),
        migrations.RemoveField(
            model_name='property',
            name='rules',
        ),
    ]
