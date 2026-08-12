"""
customers.py
------------
Handles customer registration and lookup.
"""

from db_connection import get_connection, close_connection


def add_customer(full_name, email, phone, address):
    """Registers a new customer."""
    connection = get_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO customers (full_name, email, phone, address)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (full_name, email, phone, address))
        connection.commit()
        print(f"[OK] Customer '{full_name}' registered with ID {cursor.lastrowid}.")
    except Exception as e:
        print(f"[ERROR] Failed to add customer: {e}")
    finally:
        close_connection(connection)


def find_customer_by_email(email):
    """Looks up a customer by email. Returns a dict or None."""
    connection = get_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        return cursor.fetchone()
    except Exception as e:
        print(f"[ERROR] Failed to find customer: {e}")
        return None
    finally:
        close_connection(connection)


def list_customers():
    """Returns and prints all registered customers."""
    connection = get_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers ORDER BY customer_id")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return rows
    finally:
        close_connection(connection)
