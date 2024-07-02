# utils.py
from .models import Order_7food, Order_saboyfood, OrderTable


def total_estimated_time_unprepared_orders():
    """
    Calculate the total estimated time for all unprepared orders.

    Returns:
        int: Total estimated time for all unprepared orders.
    """
    unprepared_orders = Order_saboyfood.objects.filter(prepared=False)
    total_time = sum(order.taxminiy_vaqt for order in unprepared_orders)
    return total_time

def total_estimated_time_undelivered_orders():
    """
    Calculate the total estimated time for all undelivered orders,
    considering 1.5 minutes for every 100 meters of distance.

    Returns:
        int: Total estimated time for all undelivered orders.
    """
    undelivered_orders = Order_7food.objects.filter(delivered=False)
    total_time = 0
    for order in undelivered_orders:
        if order.distance_in_meters is not None:
            distance_time = (order.distance_in_meters / 100) * 1.5
            total_time += distance_time
        total_time += order.taxminiy_vaqt
    return round(total_time)


def total_estimated_time_for_unprepared_orders_in_Table_Order_7food():
    """
    Calculate the total estimated time for all orders where status=False.

    Returns:
        int: Total estimated time for all unprepared orders.
    """
    unprepared_orders = OrderTable.objects.filter(status=False)
    total_time = sum(order.total_estimated_time for order in unprepared_orders)
    return total_time


def Sum_all_order_time():
    a = total_estimated_time_unprepared_orders() + total_estimated_time_undelivered_orders() + total_estimated_time_for_unprepared_orders_in_Table_Order_7food()
    return a




