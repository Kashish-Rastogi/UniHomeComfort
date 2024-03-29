# Generated by Django 5.0.1 on 2024-02-27 03:36

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_delete_property'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('property_type', models.CharField(choices=[('apartment', 'Apartment'), ('house', 'House'), ('condo', 'Condo')], max_length=50)),
                ('number_of_bedrooms', models.IntegerField()),
                ('number_of_bathrooms', models.IntegerField()),
                ('amenities', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('availability_status', models.CharField(choices=[('available', 'Available'), ('not_available', 'Not Available'), ('coming_soon', 'Coming Soon')], max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('available_from', models.DateTimeField(default=django.utils.timezone.now)),
                ('available_to', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_biddable', models.BooleanField(default=True)),
                ('bidding_min_limit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lease_required', models.BooleanField(default=True)),
                ('lease_duration', models.IntegerField(default=12)),
                ('allowed_lease_people', models.IntegerField(default=2)),
                ('rules', models.TextField(blank=True)),
                ('prop_image1', models.FileField(upload_to='documents/property_images/')),
                ('prop_image2', models.FileField(upload_to='documents/property_images/')),
                ('prop_image3', models.FileField(upload_to='documents/property_images/')),
                ('prop_image4', models.FileField(blank=True, null=True, upload_to='documents/property_images/')),
                ('prop_image5', models.FileField(blank=True, null=True, upload_to='documents/property_images/')),
                ('house_build_date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_name', to='mainapp.owneruser')),
            ],
        ),
    ]
