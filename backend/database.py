import sqlite3
from typing import List, Dict, Any
from datetime import datetime
import os


DATABASE_PATH = "customers.db"


def get_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Initialize database with multiple tables, relationships, and sample data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            city TEXT,
            country TEXT,
            created_at TIMESTAMP NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TIMESTAMP NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    cursor.execute("SELECT COUNT(*) as count FROM customers")
    if cursor.fetchone()["count"] == 0:
        customers_data = [
            ("Alice Johnson", "alice@example.com", "+1-555-0101", "New York", "USA", "2024-01-15 10:30:00"),
            ("Bob Smith", "bob@example.com", "+1-555-0102", "Los Angeles", "USA", "2024-02-20 14:15:00"),
            ("Charlie Brown", "charlie@example.com", "+1-555-0103", "Chicago", "USA", "2024-03-10 09:45:00"),
            ("Diana Prince", "diana@example.com", "+44-20-5550104", "London", "UK", "2024-01-05 16:20:00"),
            ("Eve Wilson", "eve@example.com", "+1-555-0105", "San Francisco", "USA", "2024-02-28 11:00:00"),
            ("Frank Miller", "frank@example.com", "+1-555-0106", "Boston", "USA", "2024-03-15 13:30:00"),
            ("Grace Lee", "grace@example.com", "+1-555-0107", "Seattle", "USA", "2023-12-01 08:00:00"),
            ("Henry Davis", "henry@example.com", "+1-555-0108", "Miami", "USA", "2024-01-20 15:45:00"),
            ("Iris Chen", "iris@example.com", "+86-10-5550109", "Beijing", "China", "2024-02-10 10:10:00"),
            ("Jack Thompson", "jack@example.com", "+1-555-0110", "Austin", "USA", "2024-03-01 12:20:00"),
            ("Kate Williams", "kate@example.com", "+1-555-0111", "Denver", "USA", "2024-01-25 09:00:00"),
            ("Leo Martinez", "leo@example.com", "+1-555-0112", "Phoenix", "USA", "2024-02-15 14:30:00"),
            ("Maya Patel", "maya@example.com", "+91-22-5550113", "Mumbai", "India", "2024-03-05 11:15:00"),
            ("Nathan Kim", "nathan@example.com", "+82-2-5550114", "Seoul", "South Korea", "2024-01-10 13:45:00"),
            ("Olivia Brown", "olivia@example.com", "+1-555-0115", "Portland", "USA", "2024-02-25 10:20:00"),
        ]
        
        cursor.executemany(
            "INSERT INTO customers (name, email, phone, city, country, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            customers_data
        )
        
        products_data = [
            ("Laptop Pro 15", "Electronics", 1299.99, 45, "2024-01-01 00:00:00"),
            ("Wireless Mouse", "Electronics", 29.99, 150, "2024-01-01 00:00:00"),
            ("Mechanical Keyboard", "Electronics", 89.99, 80, "2024-01-01 00:00:00"),
            ("USB-C Hub", "Electronics", 49.99, 120, "2024-01-01 00:00:00"),
            ("4K Monitor", "Electronics", 399.99, 30, "2024-01-01 00:00:00"),
            ("Desk Lamp LED", "Office", 34.99, 200, "2024-01-01 00:00:00"),
            ("Office Chair", "Office", 249.99, 60, "2024-01-01 00:00:00"),
            ("Standing Desk", "Office", 499.99, 25, "2024-01-01 00:00:00"),
            ("Notebook Set", "Office", 12.99, 300, "2024-01-01 00:00:00"),
            ("Wireless Headphones", "Electronics", 149.99, 90, "2024-01-01 00:00:00"),
            ("Phone Stand", "Electronics", 19.99, 180, "2024-01-01 00:00:00"),
            ("Cable Organizer", "Office", 8.99, 250, "2024-01-01 00:00:00"),
            ("Webcam HD", "Electronics", 79.99, 70, "2024-01-01 00:00:00"),
            ("Desk Mat", "Office", 24.99, 140, "2024-01-01 00:00:00"),
            ("Portable SSD 1TB", "Electronics", 129.99, 55, "2024-01-01 00:00:00"),
        ]
        
        cursor.executemany(
            "INSERT INTO products (name, category, price, stock_quantity, created_at) VALUES (?, ?, ?, ?, ?)",
            products_data
        )
        
        orders_data = [
            (1, "2024-01-16 11:20:00", 1329.98, "delivered"),
            (1, "2024-02-10 14:35:00", 89.99, "delivered"),
            (2, "2024-02-21 09:15:00", 449.98, "delivered"),
            (2, "2024-03-05 16:40:00", 1299.99, "shipped"),
            (3, "2024-03-11 10:25:00", 284.98, "delivered"),
            (4, "2024-01-06 13:50:00", 1799.96, "delivered"),
            (4, "2024-02-15 11:30:00", 179.98, "delivered"),
            (5, "2024-03-01 15:20:00", 499.99, "processing"),
            (6, "2024-03-16 09:45:00", 62.98, "pending"),
            (7, "2023-12-02 10:15:00", 2099.94, "delivered"),
            (7, "2024-01-20 14:25:00", 399.99, "delivered"),
            (8, "2024-01-21 12:40:00", 279.97, "delivered"),
            (9, "2024-02-11 16:10:00", 1429.98, "delivered"),
            (10, "2024-03-02 11:55:00", 749.97, "shipped"),
            (11, "2024-01-26 13:30:00", 524.98, "delivered"),
            (12, "2024-02-16 10:20:00", 399.99, "delivered"),
            (13, "2024-03-06 15:45:00", 179.97, "processing"),
            (14, "2024-01-11 09:25:00", 1549.98, "delivered"),
            (15, "2024-02-26 14:15:00", 279.98, "shipped"),
            (1, "2024-03-10 10:30:00", 149.99, "delivered"),
        ]
        
        cursor.executemany(
            "INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)",
            orders_data
        )
        
        order_items_data = [
            (1, 1, 1, 1299.99, 1299.99),
            (1, 2, 1, 29.99, 29.99),
            (2, 3, 1, 89.99, 89.99),
            (3, 5, 2, 399.99, 799.98),
            (3, 4, 1, 49.99, 49.99),
            (4, 1, 1, 1299.99, 1299.99),
            (5, 9, 2, 12.99, 25.98),
            (5, 7, 1, 249.99, 249.99),
            (5, 12, 1, 8.99, 8.99),
            (6, 1, 1, 1299.99, 1299.99),
            (6, 8, 1, 499.99, 499.99),
            (7, 10, 2, 149.99, 299.98),
            (7, 2, 1, 29.99, 29.99),
            (8, 8, 1, 499.99, 499.99),
            (9, 11, 1, 19.99, 19.99),
            (9, 12, 5, 8.99, 44.95),
            (10, 1, 1, 1299.99, 1299.99),
            (10, 10, 1, 149.99, 149.99),
            (11, 5, 1, 399.99, 399.99),
            (12, 7, 1, 249.99, 249.99),
            (12, 8, 1, 499.99, 499.99),
            (12, 3, 1, 89.99, 89.99),
            (13, 13, 1, 79.99, 79.99),
            (14, 5, 1, 399.99, 399.99),
            (14, 1, 1, 1299.99, 1299.99),
            (15, 2, 3, 29.99, 89.97),
            (15, 6, 1, 34.99, 34.99),
            (16, 5, 1, 399.99, 399.99),
            (17, 10, 1, 149.99, 149.99),
            (17, 2, 1, 29.99, 29.99),
            (18, 1, 1, 1299.99, 1299.99),
            (18, 7, 1, 249.99, 249.99),
            (19, 5, 1, 399.99, 399.99),
            (19, 10, 2, 149.99, 299.98),
            (20, 10, 1, 149.99, 149.99),
        ]
        
        cursor.executemany(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)",
            order_items_data
        )
        
        conn.commit()
    
    conn.close()


def execute_query(sql: str) -> List[Dict[str, Any]]:
    """
    Execute SQL query and return results
    Validates that query is SELECT only for safety
    """
    sql_stripped = sql.strip().upper()
    
    if not sql_stripped.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")
    
    if any(keyword in sql_stripped for keyword in ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE"]):
        raise ValueError("Unsafe SQL operation detected")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        return results
    except sqlite3.Error as e:
        raise ValueError(f"SQL execution error: {str(e)}")
    finally:
        conn.close()


def get_schema_info() -> str:
    """Get database schema information for LLM context"""
    schema = """
Database Schema:

Table: customers
Columns:
  - id: INTEGER (Primary Key)
  - name: TEXT (Customer full name)
  - email: TEXT (Unique email address)
  - phone: TEXT (Phone number)
  - city: TEXT (City name)
  - country: TEXT (Country name)
  - created_at: TIMESTAMP (Account creation date)

Table: products
Columns:
  - id: INTEGER (Primary Key)
  - name: TEXT (Product name)
  - category: TEXT (Product category: Electronics, Office)
  - price: REAL (Product price in USD)
  - stock_quantity: INTEGER (Available stock)
  - created_at: TIMESTAMP (Product added date)

Table: orders
Columns:
  - id: INTEGER (Primary Key)
  - customer_id: INTEGER (Foreign Key -> customers.id)
  - order_date: TIMESTAMP (Order date and time)
  - total_amount: REAL (Total order amount in USD)
  - status: TEXT (Order status: pending, processing, shipped, delivered, cancelled)

Table: order_items
Columns:
  - id: INTEGER (Primary Key)
  - order_id: INTEGER (Foreign Key -> orders.id)
  - product_id: INTEGER (Foreign Key -> products.id)
  - quantity: INTEGER (Quantity ordered)
  - unit_price: REAL (Price per unit at time of order)
  - subtotal: REAL (quantity * unit_price)

Relationships:
- customers.id <- orders.customer_id (One customer can have many orders)
- orders.id <- order_items.order_id (One order can have many items)
- products.id <- order_items.product_id (One product can be in many orders)

Sample query examples:
- SELECT * FROM customers WHERE country = 'USA';
- SELECT name, email FROM customers ORDER BY created_at DESC LIMIT 5;
- SELECT p.name, p.price, p.category FROM products p WHERE p.stock_quantity > 50;
- SELECT c.name, COUNT(o.id) as order_count FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id;
- SELECT p.name, SUM(oi.quantity) as total_sold FROM products p JOIN order_items oi ON p.id = oi.product_id GROUP BY p.id ORDER BY total_sold DESC;
- SELECT c.name, o.total_amount, o.status FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.status = 'delivered';
"""
    return schema
