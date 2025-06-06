# Generated by Django 5.2 on 2025-04-26 05:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kyc', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='kycdocument',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kyc_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='kycdocument',
            name='verified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verified_documents', to=settings.AUTH_USER_MODEL),
        ),
    ]
