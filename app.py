from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS
from modules import functions
from flask_mysqldb import MySQL  # Adding MySQL library
import pytest
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


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
@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout/')
def logout():
    return redirect('/')

# ======================= DEBUG ==========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
