from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS
from modules import functions
from flask_mysqldb import MySQL  # Adding MySQL library
import pytest
import requests

app = Flask(__name__)
CORS(app)

# Configure MySQL connection
app.config["MYSQL_HOST"] = "localhost"  # Replace with your MySQL host
app.config["MYSQL_USER"] = "dashi"       # Replace with your MySQL username
app.config["MYSQL_PASSWORD"] = "password"  # Replace with your MySQL password
app.config["MYSQL_DB"] = "csi"  # Replace with your database name
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# === Main & Admin Pages ===
@app.route('/', methods=['GET'])
def index():
    return functions.pull_products(mysql)

@app.route('/admin/')
def admin_panel():
    return render_template('admin_panel.html')

def add_new_product():
    data = request.json
    p_name = data.get("new_p_name")
    p_price = data.get("new_p_price")
    p_stock = data.get("new_p_stock")
    return functions.add_new_product(p_name , p_price , p_stock)

def change_p_name():
    data = request.json
    p_id = data.get("product_id")
    new_name = data.get("new_name")
    return functions.product_name_change(p_id , new_name)

def change_price():
    data = request.json
    p_id = data.get("product_id")
    new_price = data.get("new_price")
    return functions.price_manip(p_id , new_price)

def remove_x_stock():
    data = request.json
    p_id = data.get("product_id")
    new_stock = data.get("new_stock_less")
    return functions.remove_x_from_product_stock(p_id , new_stock)

def add_x_stock():
    data = request.json
    p_id = data.get('p_id')
    new_stock = data.get("new_stock_more")
    return functions.add_x_to_product_stock(new_stock , p_id)

def price_manip():
    data = request.json
    p_id = data.get("p_id")
    new_price = data.get("new_price")
    return functions.price_manip(p_id , new_price)

# === User Login Pages & Methods ===
@app.route('/login/', methods=['POST'])
def login():
    data = request.json
    return functions.authenticate_user(data)

@app.route('/logout/')
def logout():
    return redirect('/')

# == Cart Routes ==

@app.route('/cart/save', methods=['POST'])
def save_cart():
    data = request.json
    user_id = data.get("user_id")
    cart_items = data.get("cart_items", [])
    if not user_id or not isinstance(cart_items, list):
        return jsonify({"success": False, "message": "Invalid data format"}), 400
    return functions.save_cart(user_id, cart_items)

# === Get Cart Route ===
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    return functions.get_cart(user_id)

@app.route('/checkout', methods=['POST'])
def checkout_route():
    data = request.json
    user_id = data.get('user_id')
    cart_items = data.get('cart_items')

    # Call checkout function from functions.py
    response = functions.checkout(user_id, cart_items)
    return response

# ======================= DEBUG ==========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
