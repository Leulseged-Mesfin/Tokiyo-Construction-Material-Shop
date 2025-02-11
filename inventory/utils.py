from .models import OrderLog, Report

def create_log(user, action, model_name, object_id, details=None):
    Log.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        details=details
    )


def create_order_log(user, action, model_name, object_id, customer_info, product_name, quantity, price, changes_on_update):
    # print("Order Log Active")
    OrderLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        customer_info = customer_info,
        product_name = product_name,
        quantity = quantity,
        price = price,
        changes_on_update = changes_on_update
    )
    

def create_order_report(user, customer_name, customer_phone, customer_tin_number, order_date, product_name, product_price, quantity, price):
    # print("Order Report Active")
    Report.objects.create(
        user = user,
        customer_name = customer_name,
        customer_phone = customer_phone,
        customer_tin_number = customer_tin_number,
        order_date = order_date,
        product_name = product_name,
        product_price = product_price,
        quantity = quantity,
        price = price
    )

