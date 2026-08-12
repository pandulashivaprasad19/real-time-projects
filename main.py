"""
main.py
-------
Entry point for the E-Commerce Store Management System.
A simple menu-driven CLI that lets a user manage products,
customers, and orders backed by a MySQL database.

Run:
    python main.py
"""

import customers
import products
import orders


def products_menu():
    while True:
        print("\n--- PRODUCT MENU ---")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. List Products")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Product name: ")
            category_id = int(input("Category ID: "))
            price = float(input("Price: "))
            stock = int(input("Stock quantity: "))
            products.add_product(name, category_id, price, stock)
        elif choice == "2":
            pid = int(input("Product ID: "))
            price = input("New price (leave blank to skip): ")
            stock = input("New stock quantity (leave blank to skip): ")
            products.update_product(
                pid,
                price=float(price) if price else None,
                stock_quantity=int(stock) if stock else None
            )
        elif choice == "3":
            pid = int(input("Product ID to delete: "))
            products.delete_product(pid)
        elif choice == "4":
            products.list_products()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def customers_menu():
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. Register Customer")
        print("2. List Customers")
        print("3. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Full name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            address = input("Address: ")
            customers.add_customer(name, email, phone, address)
        elif choice == "2":
            customers.list_customers()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def orders_menu():
    while True:
        print("\n--- ORDER MENU ---")
        print("1. Place Order")
        print("2. Update Order Status")
        print("3. View Order Summary")
        print("4. Sales Report")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            customer_id = int(input("Customer ID: "))
            cart_items = []
            while True:
                pid = input("Product ID (blank to finish): ")
                if not pid:
                    break
                qty = int(input("Quantity: "))
                price = float(input("Unit price: "))
                cart_items.append({
                    "product_id": int(pid),
                    "quantity": qty,
                    "unit_price": price
                })
            orders.place_order(customer_id, cart_items)
        elif choice == "2":
            oid = int(input("Order ID: "))
            status = input("New status (PENDING/CONFIRMED/SHIPPED/DELIVERED/CANCELLED): ").upper()
            orders.update_order_status(oid, status)
        elif choice == "3":
            oid = int(input("Order ID: "))
            summary = orders.get_order_summary(oid)
            if summary:
                print(summary)
        elif choice == "4":
            orders.sales_report()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n===== E-COMMERCE STORE MANAGEMENT SYSTEM =====")
        print("1. Manage Products")
        print("2. Manage Customers")
        print("3. Manage Orders")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            products_menu()
        elif choice == "2":
            customers_menu()
        elif choice == "3":
            orders_menu()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
