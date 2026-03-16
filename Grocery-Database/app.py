import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Read DB credentials from environment variables
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_NAME = os.getenv("MYSQL_DATABASE", "grocery_db")
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASS = os.getenv("MYSQL_PASSWORD", "")


# Function to connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )


@app.route("/")
def index():
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("SELECT id, name, breed FROM cats")
    # cats = cursor.fetchall()
    # cursor.close()
    # conn.close()
    # return render_template("index.html", cats=cats)

    # Query the things that would be cool to see here
    return render_template("index.html")

@app.route("/customers")
def customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    return render_template("customers.html", customers=customers) # Customers can be access from the var

@app.route("/inventory")
def inventory():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("inventory.html", inventory=inventory)

@app.route("/orders")
def orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("orders.html", orders=orders)


if __name__ == "__main__":
    # Initialize database
    conn = get_db_connection()

    # Tables not layed out properly
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            type VARCHAR(100)
            )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age VARCHAR(100)
            )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            product VARCHAR(100)        
            )
    """)
    conn.commit()
    cursor.close()
    conn.close()

    app.run(host="0.0.0.0", port=5000, debug=True)
