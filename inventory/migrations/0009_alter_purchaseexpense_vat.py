# Generated by Django 5.1.1 on 2025-02-12 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_purchaseproduct_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseexpense',
            name='vat',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
