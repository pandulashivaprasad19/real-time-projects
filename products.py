"""
products.py
------------
Handles all product-related database operations:
add, update, delete, view, and search products, plus
stock management.
"""

from db_connection import get_connection, close_connection


def add_product(name, category_id, price, stock_quantity):
    """Inserts a new product into the products table."""
    connection = get_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO products (product_name, category_id, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, category_id, price, stock_quantity))
        connection.commit()
        print(f"[OK] Product '{name}' added with ID {cursor.lastrowid}.")
    except Exception as e:
        print(f"[ERROR] Failed to add product: {e}")
    finally:
        close_connection(connection)


def update_product(product_id, price=None, stock_quantity=None):
    """Updates price and/or stock quantity for a given product."""
    connection = get_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        if price is not None:
            cursor.execute(
                "UPDATE products SET price = %s WHERE product_id = %s",
                (price, product_id)
            )
        if stock_quantity is not None:
            cursor.execute(
                "UPDATE products SET stock_quantity = %s WHERE product_id = %s",
                (stock_quantity, product_id)
            )
        connection.commit()
        print(f"[OK] Product ID {product_id} updated.")
    except Exception as e:
        print(f"[ERROR] Failed to update product: {e}")
    finally:
        close_connection(connection)


def delete_product(product_id):
    """Deletes a product by its ID."""
    connection = get_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        connection.commit()
        print(f"[OK] Product ID {product_id} deleted.")
    except Exception as e:
        print(f"[ERROR] Failed to delete product: {e}")
    finally:
        close_connection(connection)


def list_products():
    """Returns and prints all products with category names."""
    connection = get_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT p.product_id, p.product_name, c.category_name,
                   p.price, p.stock_quantity
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            ORDER BY p.product_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return rows
    except Exception as e:
        print(f"[ERROR] Failed to fetch products: {e}")
        return []
    finally:
        close_connection(connection)


def reduce_stock(product_id, quantity):
    """Reduces stock quantity after an order is placed. Returns True on success."""
    connection = get_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT stock_quantity FROM products WHERE product_id = %s",
            (product_id,)
        )
        result = cursor.fetchone()
        if not result or result[0] < quantity:
            print(f"[ERROR] Insufficient stock for product ID {product_id}.")
            return False

        cursor.execute(
            "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
            (quantity, product_id)
        )
        connection.commit()
        return True
    except Exception as e:
        print(f"[ERROR] Failed to reduce stock: {e}")
        return False
    finally:
        close_connection(connection)
