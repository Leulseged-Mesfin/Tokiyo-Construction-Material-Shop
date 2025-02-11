# import random
# import datetime

# # Sample data for each table
# categories = [(i, f'category {i}') for i in range(1, 51)]
# suppliers = [(i, f'supplier {i}', f'contact info {i}') for i in range(1, 51)]
# products = []
# customers = []
# inventory_orders = []
# inventory_order_items = []

# # Generating INSERT statements for Categories
# print("-- Insert categories")
# for category in categories:
#     print(f"INSERT INTO inventory_category (id, name) VALUES ({category[0]}, '{category[1]}');")

# # Generating INSERT statements for Suppliers
# print("\n-- Insert suppliers")
# for supplier in suppliers:
#     print(f"INSERT INTO inventory_supplier (id, name, contact_info) VALUES ({supplier[0]}, '{supplier[1]}', '{supplier[2]}');")

# # Generating 150 Products
# for i in range(1, 151):
#     name = f'product {i}'
#     category_id = random.choice(categories)[0]
#     description = f'description for product {i}'
#     buying_price = round(random.uniform(10.00, 500.00), 2)
#     selling_price = buying_price + round(random.uniform(10.00, 100.00), 2)
#     stock = random.randint(10, 500)
#     supplier_id = random.choice(suppliers)[0]
#     image = f'path/to/image{i}.jpg'
#     products.append((i, name, category_id, description, buying_price, selling_price, stock, supplier_id, image))

# # Generating INSERT statements for Products
# print("\n-- Insert products")
# for product in products:
#     print(f"INSERT INTO inventory_product (id, name, category_id, description, buying_price, selling_price, stock, supplier_id, image) \n          VALUES ({product[0]}, '{product[1]}', {product[2]}, '{product[3]}', {product[4]}, {product[5]}, {product[6]}, {product[7]}, '{product[8]}');")

# # Generating 200 Customers
# for i in range(1, 201):
#     name = f'customer {i}'
#     phone = f'111-000-{str(i).zfill(4)}'
#     address = f'address {i}'
#     customers.append((i, name, phone, address))

# # Generating INSERT statements for Customers
# print("\n-- Insert customers")
# for customer in customers:
#     print(f"INSERT INTO inventory_customerinfo (id, name, phone, address) VALUES ({customer[0]}, '{customer[1]}', '{customer[2]}', '{customer[3]}');")

# # Generating 200 Inventory Orders
# for i in range(1, 201):
#     customer_id = random.choice(customers)[0]
#     order_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
#     status = random.choice(['Pending', 'Completed'])
#     total_amount = round(random.uniform(50.00, 1000.00), 2)
#     inventory_orders.append((i, customer_id, order_date.strftime('%Y-%m-%d %H:%M:%S'), status, total_amount))

# # Generating INSERT statements for Inventory Orders
# print("\n-- Insert inventory_orders")
# for order in inventory_orders:
#     print(f"INSERT INTO inventory_order (id, customer_id, order_date, status, total_amount) VALUES ({order[0]}, {order[1]}, '{order[2]}', '{order[3]}', {order[4]});")

# # Generating 300 Inventory Order Items
# for i in range(1, 301):
#     order_id = random.choice(inventory_orders)[0]
#     product_id = random.choice(products)[0]
#     quantity = random.randint(1, 10)
#     price = round(random.uniform(20.00, 500.00), 2)
#     inventory_order_items.append((i, order_id, product_id, quantity, price))

# # Generating INSERT statements for Inventory Order Items
# print("\n-- Insert inventory_order_items")
# for item in inventory_order_items:
#     print(f"INSERT INTO inventory_orderitem (id, order_id, product_id, quantity, price) VALUES ({item[0]}, {item[1]}, {item[2]}, {item[3]}, {item[4]});")



import random
import datetime
import uuid

# Sample data for each table
categories = [(i, f'Electronics {i}') if i % 2 == 0 else (i, f'Home Appliances {i}') for i in range(1, 51)]
suppliers = [(i, f'Supplier {uuid.uuid4().hex[:8]}', f'{random.randint(100, 999)}-555-{str(i).zfill(4)}') for i in range(1, 51)]
products = []
customers = []
inventory_orders = []
inventory_order_items = []
existing_order_item_ids = set()  # Track unique (id, order_id) combinations

# Generating INSERT statements for Categories
print("-- Insert categories")
for category in categories:
    print(f"INSERT INTO inventory_category (id, name) VALUES ({category[0]}, '{category[1]}');")

# Generating INSERT statements for Suppliers
print("\n-- Insert suppliers")
for supplier in suppliers:
    print(f"INSERT INTO inventory_supplier (id, name, contact_info) VALUES ({supplier[0]}, '{supplier[1]}', '{supplier[2]}');")

# Generating 150 Products with diverse naming and description patterns
product_names = ["Laptop", "Smartphone", "Microwave", "Air Conditioner", "Headphones", "Refrigerator", "Oven", "Washing Machine", "Camera", "Printer"]
for i in range(1, 151):
    name = f'{random.choice(product_names)} Model-{random.randint(1000, 9999)}'
    category_id = random.choice(categories)[0]
    description = f'{name} with advanced features and great performance.'
    buying_price = round(random.uniform(50.00, 1000.00), 2)
    selling_price = buying_price + round(random.uniform(10.00, 200.00), 2)
    stock = random.randint(5, 300)
    supplier_id = random.choice(suppliers)[0]
    image = f'images/products/{uuid.uuid4().hex[:12]}.jpg'
    products.append((i, name, category_id, description, buying_price, selling_price, stock, supplier_id, image))

# Generating INSERT statements for Products
print("\n-- Insert products")
for product in products:
    print(f"INSERT INTO inventory_product (id, name, category_id, description, buying_price, selling_price, stock, supplier_id, image) \n          VALUES ({product[0]}, '{product[1]}', {product[2]}, '{product[3]}', {product[4]}, {product[5]}, {product[6]}, {product[7]}, '{product[8]}');")

# Generating 200 Customers with realistic data
customer_first_names = ["John", "Jane", "Michael", "Emily", "David", "Sophia", "Daniel", "Olivia", "James", "Emma"]
customer_last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
for i in range(1, 201):
    name = f'{random.choice(customer_first_names)} {random.choice(customer_last_names)}'
    phone = f'({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}'
    address = f'{random.randint(1, 9999)} {random.choice(["Main St", "Elm St", "2nd Ave", "Maple St", "Park Blvd"])}'
    customers.append((i, name, phone, address))

# Generating INSERT statements for Customers
print("\n-- Insert customers")
for customer in customers:
    print(f"INSERT INTO inventory_customerinfo (id, name, phone, address) VALUES ({customer[0]}, '{customer[1]}', '{customer[2]}', '{customer[3]}');")

# Generating 200 Inventory Orders with correct total_amount
print("\n-- Insert inventory_orders")
for i in range(1, 201):
    customer_id = random.choice(customers)[0]
    order_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 730))
    status = random.choice(['Pending', 'Completed'])
    order_items = []
    total_amount = 0

    # Add a random number of items (at least one) to each order
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product = random.choice(products)
        product_id = product[0]
        selling_price = product[5]  # Use the selling_price from the product
        quantity = random.randint(1, 10)
        price = round(selling_price, 2)
        item_id = len(inventory_order_items) + 1

        # Ensure uniqueness of (id, order_id) combination
        while (item_id, i) in existing_order_item_ids:
            item_id += 1  # Increment item_id until unique (id, order_id) is found

        existing_order_item_ids.add((item_id, i))  # Add the (id, order_id) pair to the set
        order_items.append((item_id, i, product_id, quantity, price))
        total_amount += price * quantity

    inventory_orders.append((i, customer_id, order_date.strftime('%Y-%m-%d %H:%M:%S'), status, round(total_amount, 2)))

    # Add the items to the inventory_order_items list
    for item in order_items:
        inventory_order_items.append(item)

# Generating INSERT statements for Inventory Orders
for order in inventory_orders:
    print(f"INSERT INTO inventory_order (id, customer_id, order_date, status, total_amount) VALUES ({order[0]}, {order[1]}, '{order[2]}', '{order[3]}', {order[4]});")

# Generating INSERT statements for Inventory Order Items
print("\n-- Insert inventory_order_items")
for item in inventory_order_items:
    print(f"INSERT INTO inventory_orderitem (id, order_id, product_id, quantity, price) VALUES ({item[0]}, {item[1]}, {item[2]}, {item[3]}, {item[4]});")
