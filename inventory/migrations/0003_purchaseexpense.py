# Generated by Django 5.1.1 on 2025-02-12 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_companyinfo_bank_accounts_performa'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(blank=True, default='Pcs', max_length=255, null=True)),
                ('unit', models.CharField(blank=True, default='Pcs', max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('vat', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('unpaid_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
            ],
        ),
    ]
