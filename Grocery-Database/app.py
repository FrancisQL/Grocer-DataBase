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

@app.route("/customers", methods=["GET", "POST"])
def customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # If the form was submitted
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]

        cursor.execute(
            "INSERT INTO customers (name, address) VALUES (%s, %s)",
            (name, address)
        )
        conn.commit()

        return redirect(url_for("customers"))

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    return render_template("customers.html", customers=customers) # Customers can be access from the var

@app.route("/inventory", methods=["GET", "POST"])
def inventory():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # If the form was submitted
    if request.method == "POST":
        product_ID = request.form["product_ID"]
        stock_Level = request.form["stockLevel"]

        cursor.execute(
            "INSERT INTO inventory (product_ID, stockLevel) VALUES (%s, %s)",
            (product_ID, stock_Level)
        )
        conn.commit()

        return redirect(url_for("inventory"))

    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("inventory.html", inventory=inventory)

@app.route("/orders", methods=["GET", "POST"])
def orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Will also need to add items that were on the order somehow
    if request.method == "POST":
        name = request.form["name"]
        type = request.form["type"]
        total = request.form["total"]
        customer_id = request.form["customer_id"]

        cursor.execute(
            "INSERT INTO orders (name, customer_id, total, type) VALUES (%s, %s, %s, %s)",
            (name, customer_id, total, type)
        )
        conn.commit()

        return redirect(url_for("orders"))

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("orders.html", orders=orders)

@app.route("/products", methods=["GET", "POST"])
def products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # If the form was submitted
    if request.method == "POST":
        name = request.form["name"]

        cursor.execute(
            "INSERT INTO products (name) VALUES (%s)", (name,) # Comma added to create a tuple
        )
        conn.commit()

        return redirect(url_for("products"))

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("products.html", products=products)

if __name__ == "__main__":
    # Initialize database
    conn = get_db_connection()

    # Tables not layed out properly
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100)
            )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            address VARCHAR(255)
            )
    """)

    # needs to reference cusotmer ID
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            cusomter_id int,
            total int,
            type VARCHAR(100)
            )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INT AUTO_INCREMENT PRIMARY KEY,
        stockLevel INT,
        product_ID INT,
        FOREIGN KEY (product_ID) REFERENCES products(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    app.run(host="0.0.0.0", port=5000, debug=True)
