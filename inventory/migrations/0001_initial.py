# Generated by Django 5.1.1 on 2025-02-11 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True)),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Customer', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('tin_number', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
                ('action', models.CharField(blank=True, choices=[('Create', 'Create'), ('Update', 'Update'), ('Delete', 'Delete')], max_length=10, null=True)),
                ('model_name', models.CharField(blank=True, max_length=50, null=True)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('customer_info', models.CharField(blank=True, default='Customer', max_length=255, null=True)),
                ('product_name', models.CharField(blank=True, default='Product', max_length=255, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('changes_on_update', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, default='user', max_length=50, null=True)),
                ('customer_name', models.CharField(blank=True, default='Customer', max_length=255, null=True)),
                ('customer_phone', models.CharField(blank=True, default='Customer', max_length=255, null=True)),
                ('customer_tin_number', models.CharField(blank=True, default='Customer', max_length=255, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('product_name', models.CharField(blank=True, default='Product', max_length=255, null=True)),
                ('product_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('contact_info', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Company', max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('phone1', models.CharField(blank=True, max_length=255, null=True)),
                ('phone2', models.CharField(blank=True, max_length=255, null=True)),
                ('tin_number', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company/')),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('name', 'tin_number'), name='unique_company_fields')],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=100, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.customerinfo')),
            ],
        ),
        migrations.CreateModel(
            name='OtherExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
                ('expense_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.expensetypes')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('buying_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('receipt', models.BooleanField(default=False)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('user', models.CharField(blank=True, default='User', max_length=255, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.category')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('receipt', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.product')),
            ],
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('name', 'category'), name='unique_product_category'),
        ),
    ]
