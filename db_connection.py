"""
db_connection.py
-----------------
Handles the MySQL database connection for the E-Commerce Store
Management System. Uses mysql-connector-python.

Update the DB_CONFIG dictionary with your own MySQL credentials
before running the application.
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "ecommerce_db"
}


def get_connection():
    """
    Creates and returns a new MySQL database connection.
    Returns None if the connection fails.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"[ERROR] Could not connect to MySQL: {e}")
        return None


def close_connection(connection):
    """Safely closes a database connection if it is open."""
    if connection and connection.is_connected():
        connection.close()
