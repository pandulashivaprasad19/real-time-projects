"""
orders.py
---------
Handles order placement, order-item creation, stock deduction,
and order status/report queries.
"""

from db_connection import get_connection, close_connection
from products import reduce_stock


def place_order(customer_id, cart_items):
    """
    Places a new order.

    cart_items: list of dicts, each like:
        {"product_id": 1, "quantity": 2, "unit_price": 199.00}

    Returns the new order_id, or None on failure.
    """
    connection = get_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor()

        # Create the order shell first
        cursor.execute(
            "INSERT INTO orders (customer_id, order_status, total_amount) "
            "VALUES (%s, 'PENDING', 0)",
            (customer_id,)
        )
        order_id = cursor.lastrowid

        total_amount = 0.0
        for item in cart_items:
            product_id = item["product_id"]
            quantity = item["quantity"]
            unit_price = item["unit_price"]

            # Deduct stock; abort the whole order if any item is out of stock
            if not reduce_stock(product_id, quantity):
                connection.rollback()
                print(f"[ERROR] Order aborted — insufficient stock for product {product_id}.")
                return None

            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) "
                "VALUES (%s, %s, %s, %s)",
                (order_id, product_id, quantity, unit_price)
            )
            total_amount += quantity * float(unit_price)

        cursor.execute(
            "UPDATE orders SET total_amount = %s, order_status = 'CONFIRMED' WHERE order_id = %s",
            (total_amount, order_id)
        )
        connection.commit()
        print(f"[OK] Order {order_id} placed successfully. Total: {total_amount:.2f}")
        return order_id

    except Exception as e:
        connection.rollback()
        print(f"[ERROR] Failed to place order: {e}")
        return None
    finally:
        close_connection(connection)


def update_order_status(order_id, status):
    """Updates the status of an order (e.g., SHIPPED, DELIVERED, CANCELLED)."""
    valid_statuses = {"PENDING", "CONFIRMED", "SHIPPED", "DELIVERED", "CANCELLED"}
    if status not in valid_statuses:
        print(f"[ERROR] Invalid status '{status}'.")
        return

    connection = get_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE orders SET order_status = %s WHERE order_id = %s",
            (status, order_id)
        )
        connection.commit()
        print(f"[OK] Order {order_id} status updated to {status}.")
    finally:
        close_connection(connection)


def get_order_summary(order_id):
    """Fetches order header + line items for a given order_id."""
    connection = get_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            print(f"[ERROR] Order {order_id} not found.")
            return None

        cursor.execute(
            """
            SELECT oi.product_id, p.product_name, oi.quantity, oi.unit_price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = %s
            """,
            (order_id,)
        )
        order["items"] = cursor.fetchall()
        return order
    finally:
        close_connection(connection)


def sales_report():
    """Returns total revenue and number of orders grouped by status."""
    connection = get_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT order_status, COUNT(*) AS order_count, SUM(total_amount) AS revenue
            FROM orders
            GROUP BY order_status
            """
        )
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return rows
    finally:
        close_connection(connection)
