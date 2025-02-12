from django.db import models
from user.models import UserAccount
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from django.db.models import Sum
from decimal import Decimal



class OrderLog(models.Model):
    ACTION_CHOICES = [
        ('Create', 'Create'),
        ('Update', 'Update'),
        ('Delete', 'Delete'),
    ]
    
    user = models.CharField(max_length=255, default="User", null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, null=True, blank=True)
    model_name = models.CharField(max_length=50, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)  # ID of the object affected
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_info = models.CharField(max_length=255, default="Customer", null=True, blank=True)
    product_name = models.CharField(max_length=255, default="Product", null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    changes_on_update = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.action} - {self.model_name} ({self.object_id}) at {self.timestamp}"

class Category(models.Model):
    name = models.CharField(max_length=100, default='', unique=True)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    contact_info = models.CharField(max_length=50, null=True, blank=True)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    receipt = models.BooleanField(default=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'category'], name='unique_product_category')
        ]

    def __str__(self):
        return self.name

class CustomerInfo(models.Model):
    name = models.CharField(max_length=255, default="Customer", null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    tin_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)

    def __str__(self):
        return self.name

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255, default="Company", null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone1 = models.CharField(max_length=255, null=True, blank=True)
    phone2 = models.CharField(max_length=255, null=True, blank=True)
    bank_accounts = models.JSONField(default=dict, null=True, blank=True)
    tin_number = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to='company/', null=True, blank=True)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'tin_number'], name='unique_company_fields')
        ]

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(CustomerInfo, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=(('Pending', 'Pending'), ('Completed', 'Completed')), null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)

    def str(self):
        return self.customer
    
    # @property
    def is_empty(self):
        return not self.items.exists() 

    def get_total_price(self):
        """Calculate the total price of the entire order."""
        return sum(item.get_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    receipt = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Automatically set receipt to True if the product's receipt is True"""
        if self.product and self.product.receipt:
            self.receipt = True
        super().save(*args, **kwargs)

    def str(self):
        return self.product
    
    def get_price(self):
        """Calculate the total price of this item."""
        # return self.product.selling_price * self.quantity
        return self.price  # Now it returns the stored price
    
    def get_cost(self):
        """Calculate the total price of this item."""
        return self.product.buying_price * self.quantity

class Report(models.Model):
    user = models.CharField(max_length=50, default="user", blank=True, null=True)
    customer_name = models.CharField(max_length=255, default="Customer", null=True, blank=True)
    customer_phone = models.CharField(max_length=255, default="Customer", null=True, blank=True)
    customer_tin_number = models.CharField(max_length=255, default="Customer", null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    product_name = models.CharField(max_length=255, default="Product", null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)

    def __str__(self):
        return self.user

class ExpenseTypes(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)
    
    def __str__(self):
        return self.name

class OtherExpenses(models.Model):
    expense_type = models.ForeignKey(ExpenseTypes, on_delete=models.SET_NULL, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)

    def __str__(self):
        return self.name

class Performa(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    unit = models.CharField(max_length=255, default="Pcs", null=True, blank=True)
    customer = models.ForeignKey(CustomerInfo, on_delete=models.SET_NULL, blank=True, null=True)
    customer_tin = models.CharField(max_length=255, default="1111", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    issued_date = models.DateTimeField(auto_now_add=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)    
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)

    def __str__(self):
        return f"{self.customer.name} - {self.order_date}"

class PurchaseExpense(models.Model):
    status=(
        ('Paid','Paid'),
        ('Unpaid','Unpaid'),
        ('Pending','Pending')
    )
    sub_total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    vat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=50, choices=status, default='Pending')
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, null=True, blank=True)
    unpaid_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, null=True, blank=True)
    user = models.CharField(max_length=255, default="User", null=True, blank=True)

    def update_totals(self):
        """ Updates total amounts based on related PurchaseProduct instances. """
        if self.pk:  # Ensure the instance is saved first
            self.sub_total = self.products.aggregate(Sum('total_price'))['total_price__sum'] or 0.00
            vat_rate = Decimal('0.15')
            self.vat = self.sub_total * vat_rate
            self.total = self.sub_total + self.vat
            self.save(update_fields=['sub_total', 'vat', 'total'])  # Prevent infinite recursion
   
    def update_payment_amount(self):
        """ Updates unpaid amount based on payment status. """
        total = Decimal(str(self.total or 0))  # Convert to Decimal
        paid = Decimal(str(self.paid_amount or 0))  # Convert to Decimal

        if self.payment_status == 'Pending':
            self.unpaid_amount = max(total - paid, Decimal('0.00'))

        elif self.payment_status == 'Unpaid':
            self.paid_amount = Decimal('0.00')
            self.unpaid_amount = total

        elif self.payment_status == 'Paid':
            self.paid_amount = total
            self.unpaid_amount = Decimal('0.00')

    def save(self, *args, **kwargs):
        """ First save instance, then update fields to avoid data loss. """
        if not self.pk:  # If object is not yet saved
            super().save(*args, **kwargs)  # Save first
        
        self.update_payment_amount()  # Update values

        # Save again only if there are changes
        super().save(update_fields=['paid_amount', 'unpaid_amount'])

    def __str__(self):
        return f"{self.user} - {self.total}"

class PurchaseProduct(models.Model):
    product = models.CharField(max_length=255, default="Product", null=True, blank=True)
    unit = models.CharField(max_length=255, default="Pcs", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    expense = models.ForeignKey('PurchaseExpense', related_name='products', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super(PurchaseProduct, self).save(*args, **kwargs)

        # Update totals AFTER saving (avoids infinite recursion)
        if self.expense:
            self.expense.update_totals()

    def __str__(self):
        return f"{self.description} - {self.total_price}"


@receiver(pre_save, sender=OrderItem)
def set_order_item_price(sender, instance, **kwargs):
    """Calculate price before saving the OrderItem instance."""
    instance.price = instance.get_price()

@receiver(pre_save, sender=OrderItem)
def set_order_item_cost(sender, instance, **kwargs):
    """Calculate price before saving the OrderItem instance."""
    instance.cost = instance.get_cost()

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """Update total amount in Order when an OrderItem is added, updated, or deleted."""
    order = instance.order
    order.total_amount = order.get_total_price()
    order.save()

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    total = sum(item.quantity * item.product.selling_price for item in order.items.all())
    order.total_amount = total
    order.save()

@receiver(post_delete, sender=OrderItem)
def delete_order_if_no_items(sender, instance, **kwargs):
    # Check if the associated order has any items left
    order = instance.order
    if not order.items.exists():  # Check if the related items queryset is empty
        order.delete()