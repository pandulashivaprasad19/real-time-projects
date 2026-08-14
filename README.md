# E-Commerce Store Management System

A menu-driven **Python + MySQL** application that simulates the backend
of an online store. It manages products, customers, and orders using
a normalized relational schema, with real-time stock updates and
sales reporting.

## Features

- **Product Management** — add, update, delete, and list products with category mapping and live stock levels
- **Customer Management** — register customers and look them up by email
- **Order Processing** — place multi-item orders, automatically deduct stock, and calculate order totals
- **Order Tracking** — update order status (Pending → Confirmed → Shipped → Delivered/Cancelled)
- **Sales Reporting** — aggregate revenue and order counts grouped by status
- **Data Integrity** — foreign keys, transactional rollbacks on failed orders, and stock-availability checks before confirming an order

## Tech Stack

- **Language:** Python 3
- **Database:** MySQL
- **Connector:** `mysql-connector-python`
- **Interface:** Command-line (menu-driven)

## Project Structure

```
ecommerce_project/
├── schema.sql          # Database schema (tables, keys, seed data)
├── db_connection.py    # MySQL connection handler
├── products.py         # Product CRUD operations
├── customers.py        # Customer registration & lookup
├── orders.py           # Order placement, status updates, sales report
├── main.py             # CLI entry point / menu system
├── requirements.txt    # Python dependencies
└── README.md
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/ecommerce-python-mysql.git
   cd ecommerce-python-mysql
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create the database**
   ```bash
   mysql -u root -p < schema.sql
   ```

4. **Configure credentials**
   Update `DB_CONFIG` in `db_connection.py` with your MySQL username, password, and host.

5. **Run the application**
   ```bash
   python main.py
   ```

## Database Schema

| Table | Description |
|---|---|
| `customers` | Customer profile details |
| `categories` | Product categories |
| `products` | Product catalog with price and stock |
| `orders` | Order header (customer, status, total) |
| `order_items` | Line items linking orders to products |

## Example Workflow

1. Register a customer
2. Add products to the catalog
3. Place an order (stock is validated and deducted automatically)
4. Update order status as it moves through fulfillment
5. Generate a sales report

## Future Enhancements

- REST API layer using Flask/FastAPI
- Web-based front end
- User authentication and role-based access (admin vs. customer)
- Payment gateway integration
- Discount/coupon system


