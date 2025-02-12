# Generated by Django 5.1.1 on 2025-02-12 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_purchaseproduct_remove_purchaseexpense_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseexpense',
            name='products',
        ),
        migrations.AddField(
            model_name='purchaseproduct',
            name='expense',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.purchaseexpense'),
        ),
    ]
