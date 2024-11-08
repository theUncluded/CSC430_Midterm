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

# === User Login Pages & Methods ===
@app.route('/login/', methods=['POST'])
def login():
    data = request.json
    return functions.authenticate_user(data)  # Delegate to authenticate_user

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

    # Save cart items for the user
    return functions.save_cart(user_id, cart_items)

# === Get Cart Route ===
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    # Retrieve cart items for the user
    return functions.get_cart(user_id)



# ======================= DEBUG ==========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
