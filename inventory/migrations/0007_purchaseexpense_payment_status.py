# Generated by Django 5.1.1 on 2025-02-12 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_remove_purchaseexpense_products_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseexpense',
            name='payment_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('Pending', 'Pending')], default='Pending', max_length=50),
        ),
    ]
