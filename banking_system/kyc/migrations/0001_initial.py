# Generated by Django 5.2 on 2025-04-26 05:34

import kyc.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KYCDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('passport', 'Passport'), ('drivers_license', "Driver's License"), ('national_id', 'National ID'), ('utility_bill', 'Utility Bill')], max_length=20)),
                ('document_number', models.CharField(max_length=50)),
                ('document_file', models.FileField(upload_to=kyc.models.kyc_document_path)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'KYC Document',
                'verbose_name_plural': 'KYC Documents',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
