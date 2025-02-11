from rest_framework import serializers
from .models import Product, Supplier, Order, OrderItem, CustomerInfo,  Category, CompanyInfo, OrderLog, Report, ExpenseTypes, OtherExpenses
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from user.models import UserAccount
from user.serializers import UserSerializer
from .utils import create_order_log, create_order_report


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
    
    def create(self, validated_data, user=None):
        if user:
            validated_data['user'] = user.name
        return super().create(validated_data)
        
class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'
    
    def create(self, validated_data, user=None):
        # Add the user to the validated_data if provided
        if user:
            validated_data['user'] = user.name
        return super().create(validated_data)

class ProductGetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_name', 'description', 'buying_price', 'selling_price', 'stock', 'supplier_name', 'image', 'user']
        constraints = [
            UniqueConstraint(fields=['name', 'category_name'], name='unique_product_category')
        ]

class ProductPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        constraints = [
            UniqueConstraint(fields=['name', 'category'], name='unique_product_category')
        ]
    
    def create(self, validated_data, user=None):
        # Add the user to the validated_data if provided
        if user:
            validated_data['user'] = user.name
        return super().create(validated_data)

class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = '__all__'
    
    def create(self, validated_data, user=None):
        # Add the user to the validated_data if provided
        if user:
            validated_data['user'] = user.name
        return super().create(validated_data)

class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
        constraints = [
            UniqueConstraint(fields=['name', 'tin_number'], name='unique_company_fields')
        ]
    
    def create(self, validated_data, user=None):
        # Add the user to the validated_data if provided
        if user:
            validated_data['user'] = user.name
        return super().create(validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # Read-only
    # product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.CharField(source='product.selling_price', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_price', 'quantity', 'price']
        extra_kwargs = {
            'order': {'required': False},  # Make 'order' optional in the request
            'price': {'read_only': True}, # Make 'price' read-only if calculated
        }

    def update(self, instance, validated_data):
        # Update order fields directly
        new_quantity = validated_data.get('quantity', instance.quantity)
        product = instance.product  # Access the product from the existing order item
        # print(product.stock)    

        if new_quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        # Calculate the difference between new and existing quantity
        quantity_difference = new_quantity - instance.quantity
        # print(quantity_difference)

        # Check stock availability based on the difference
        if product.stock >= quantity_difference:
            # print(product.stock)
            product.stock -= quantity_difference  # Adjust stock by the difference
            product.save()
        else:
            raise ValidationError(f"Insufficient stock for {product.name}. Available stock is {product.stock}, but {new_quantity} was requested.")
        # print(product.stock)
        # Update the instance's quantity
        instance.quantity = new_quantity
        instance.save()

        return instance

class OrderGetSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    customer = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'order_date', 'total_amount', 'items', 'user']
        # fields = ['customer', 'status', 'items']
        extra_kwargs = {
            # 'items': {'read_only': True}, # Make 'items' read-only
            'total_amount': {'required': False},
            'total_amount': {'read_only': True}, # Make 'total_amount' read-only
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['customer', 'status', 'order_date', 'total_amount', 'items', 'user']
        extra_kwargs = {
            # 'items': {'read_only': True}, # Make 'items' read-only
            'total_amount': {'required': False},
            'total_amount': {'read_only': True}, # Make 'total_amount' read-only
        }
    
    def create(self, validated_data, user=None):
        user = self.context["request"].user
        if user:
            validated_data['user'] = user.name

        items_data = validated_data.pop('items')
        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Create the Order instance           
            order = Order.objects.create(**validated_data)

            # Create each OrderItem
            for item_data in items_data:
                # The total price 
                total_price = item_data.get('product').selling_price * item_data['quantity']
                # This will call OrderItemSerializer.validate() for each item
                product = item_data['product']
                quantity = item_data['quantity']
                # product_price = item_data['product'].selling_price
                if quantity <= 0:
                    raise ValidationError("Quantity must be greater than zero.")
                

                if product.stock >= quantity:  # Ensure there is enough stock
                    product.stock -= quantity  # Reduce stock by the order quantity
                    product.save()
                else:
                    raise ValidationError(f"Insufficient stock for {product.name}. Available stock is {product.stock}, but {instance.quantity} was requested.")

                # Create the OrderItem and associate with the Order
                OrderItem.objects.create(order=order, **item_data)
                # Adding it into the log with every itration
                create_order_log(
                    user = user.name,
                    action="Create",
                    model_name="Order",
                    object_id=order.id,
                    customer_info = order.customer,
                    product_name = item_data['product'].name,
                    quantity = item_data['quantity'],
                    price = total_price,
                    changes_on_update = "Created Order Item",
                )
                # Adding it into the report with every itration
                if order.customer is None:
                    create_order_report(
                        user = user.name,
                        customer_name = "Anonymous Customer",
                        customer_phone = "0000000000",
                        customer_tin_number = "1111",
                        order_date = order.order_date,
                        product_name = item_data['product'].name,
                        product_price = item_data['product'].selling_price,
                        quantity = item_data['quantity'],
                        price = total_price
                    )
                else:
                    create_order_report(
                        user = user.name,
                        customer_name = order.customer.name,
                        customer_phone = order.customer.phone,
                        customer_tin_number = order.customer.tin_number,
                        order_date = order.order_date,
                        product_name = item_data['product'].name,
                        product_price = item_data['product'].selling_price,
                        quantity = item_data['quantity'],
                        price = total_price
                    )

            return order
    
    
    def update(self, instance, validated_data):
        # Update order fields directly
        instance.customer = validated_data.get('customer', instance.customer)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Update nested items
        items_data = validated_data.pop('items', [])

        # If there are new items in the request, update or create them
        if items_data:
            # Iterate through the provided items data
            for item_data in items_data:
                product = item_data['product']
                new_quantity = item_data['quantity']

                
                if new_quantity <= 0:
                    raise ValidationError("Quantity must be greater than zero.")

                # Find the existing OrderItem or create a new one
                order_item = instance.items.filter(product=product).first()

                # Calculate the difference between new and existing quantity
                quantity_difference = new_quantity - order_item.quantity

                # Check stock availability based on the difference
                if product.stock >= quantity_difference:
                    product.stock -= quantity_difference  # Adjust stock by the difference
                    product.save()

                if order_item:
                    # If the item exists, update the quantity
                    order_item.quantity = new_quantity
                    order_item.save()
                else:
                    # If the item doesn't exist, create a new one
                    OrderItem.objects.create(order=instance, **item_data)
                
                

                

        return instance

class OrderLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderLog
        fields = '__all__'

class OrderReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'

class ExpenseTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseTypes
        fields = '__all__'
    
    def create(self, validated_data, user=None):
        if user:
            validated_data['user'] = user.name
        return super().create(validated_data)

class OtherExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherExpenses
        fields = '__all__'

    def create(self, validated_data, user=None):
        if user:
            validated_data['user'] = user.name
        return super().create(validated_data)


class OtherExpensesGetSerializer(serializers.ModelSerializer):
    expense_type = serializers.CharField(source='expense_type.name', read_only=True)

    class Meta:
        model = OtherExpenses
        fields = '__all__'

    def create(self, validated_data, user=None):
        if user:
            validated_data['user'] = user.name
        return super().create(validated_data)

class ProductGetReportSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_name', 'description', 'buying_price', 'selling_price', 'stock', 'supplier_name', 'user']