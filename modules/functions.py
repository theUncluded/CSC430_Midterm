import mysql.connector
import bcrypt
import json
import decimal

from flask import jsonify
from MySQLdb.cursors import DictCursor

from flask import jsonify

# =======================GLOBAL VARS & FXs=======================
ERROR_EMAIL_NOTFOUND = f"EMAIL %s NOT FOUND IN OUR SYSTEM. PLEASE REGISTER OR USE A DIFFERENT EMAIL"

#serialize instance for decimals as they cannot be serialized in/with JSON
def dec_serializer(o):
    if isinstance(o, decimal.Decimal):
        return float(o)


# =======================SQL ACTIONS=======================
#connects to db and returns db obj as future callable
def conn_2_db():
    mydb = mysql.connector.connect(#could potentially make this configurable
        host = "localhost",
        user = "dashi",
        password = "password",
        database = "csi"
    )
    return mydb
#outter vars meant for future functions
mydb = conn_2_db()
cursor = mydb.cursor(buffered=True)

#call to close connection to db
def close_conn_2_db():
    cursor.close()
    mydb.close() 

def pull_products(mysql):
    try:
        # Initialize a cursor with DictCursor to get rows as dictionaries
        cursor = mysql.connection.cursor(DictCursor)
        
        # Execute the query
        QUERY = "SELECT * FROM product;"
        cursor.execute(QUERY)
        
        # Fetch all rows as dictionaries
        result = cursor.fetchall()
        
        cursor.close()  # Close the cursor after fetching data
        
        # Log and return JSON-formatted data
        print("Products data being returned:", result)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error in pull_products: {e}")
        return jsonify({"error": "Failed to fetch products"}), 500

# ======================= Cart Functions ==========================
#assign user to cart table, try NOT to thread this with other existing carts
def assign_to_cart(users_id):
    try:
        # Check if user has a cart
        select_query = "SELECT cart_id FROM cart WHERE users_id = %s LIMIT 1"
        cursor.execute(select_query, (users_id,))
        cart_id = cursor.fetchone()
        
        # If a cart exists, return the cart id
        if cart_id:
            return cart_id[0]
        
        # If no cart exists, create a new one for the user
        insert_query = "INSERT INTO cart (users_id) VALUES (%s)"
        cursor.execute(insert_query, (users_id,))
        mydb.commit()
        return cursor.lastrowid  # Return the newly created cart ID

    except Exception as e:
        print(f"Error in assign_to_cart: {e}")
        return None

#updates the current cart to be the most recently created cart
def current_cart_db_update(users_email):
    
    MOST_RECENT_CART_QUERY = f"""update users
    set current_cart_id = (select max(cart_id) from cart where cart.users_id = users.users_id)
    where users_email = {users_email}
    """

    cursor.execute(MOST_RECENT_CART_QUERY)
def save_cart(user_id, cart_items):
    try:
        print(f"Received user_id: {user_id}, cart_items: {cart_items}")
        
        # Get or create the user's cart ID
        cart_id = assign_to_cart(user_id)
        if not cart_id:
            print("Failed to assign or retrieve cart ID.")
            return jsonify({"success": False, "message": "Failed to assign cart"}), 500

        # delete old items
        delete_query = "DELETE FROM product_pair WHERE cart_id = %s"
        cursor.execute(delete_query, (cart_id,))
        print(f"Cleared existing items in product_pair for cart_id: {cart_id}")

        # Insert updated items into product_pair
        insert_query = "INSERT INTO product_pair (cart_id, product_id, product_amount) VALUES (%s, %s, %s)"
        for item in cart_items:
            product_id = item.get("product_id")
            quantity = item.get("quantity")
            print(f"Attempting to insert product_id: {product_id}, quantity: {quantity}")
            
            if not product_id or not quantity:
                print("Invalid item data detected in cart_items:", item)
                continue
            
            cursor.execute(insert_query, (cart_id, product_id, quantity))

        mydb.commit()
        print("Cart saved successfully.")
        return jsonify({"success": True, "message": "Cart saved successfully"}), 200

    except Exception as e:
        print(f"Error in save_cart function: {e}")
        return jsonify({"success": False, "message": "Failed to save cart"}), 500

def get_cart(user_id):
    try:
        # Get the user's cart ID
        cart_id = assign_to_cart(user_id)
        if not cart_id:
            return jsonify([]), 200  # If no cart, return an empty list

        #get all items that are associated with teh cart
        select_query = """
            SELECT product_id, product_amount 
            FROM product_pair 
            WHERE cart_id = %s
        """
        cursor.execute(select_query, (cart_id,))
        result = cursor.fetchall()
        cart_items = [{"product_id": row[0], "quantity": row[1]} for row in result]
        
        return jsonify(cart_items), 200
    except Exception as e:
        print(f"Error retrieving cart: {e}")
        return jsonify({"success": False, "message": "Failed to retrieve cart"}), 500
    
def checkout(user_id, cart_items):
    try:
        cursor.execute("START TRANSACTION;")        
        for item in cart_items:
            product_id = item['product_id']
            quantity = item['quantity']        
            cursor.execute("SELECT stock FROM product WHERE product_id = %s;", (product_id,))
            stock = cursor.fetchone()[0]        
            if stock >= quantity:
                new_stock = stock - quantity
                cursor.execute("UPDATE product SET stock = %s WHERE product_id = %s;", (new_stock, product_id))
            else:
        
                cursor.execute("ROLLBACK;")
                return jsonify({"success": False, "message": f"Insufficient stock for product ID {product_id}."})
        cursor.execute("COMMIT;")
        return jsonify({"success": True, "message": "Checkout successful!"})

    except Exception as e:
        print(f"Checkout error: {e}")
        cursor.execute("ROLLBACK;")  
        return jsonify({"success": False, "message": "Checkout failed due to an error."})
# ======================= User & Account Functions ==========================

def hash_password(password):
    salt = bcrypt.gensalt()#generates a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)# Hashs the password with the salt after converting it into binary
    return hashed_password #returns the now hased password

# Function to create a cart and update current cart given a users id.
def create_cart_for_user(users_id):
    q3 = "INSERT INTO cart (users_id) VALUES (%s);"
    q4 = """
        UPDATE users 
        SET current_cart_id = (SELECT MAX(cart_id) FROM cart WHERE cart.users_id = users.users_id)
        WHERE users_id = %s;
    """
    cursor.execute(q3,(users_id,))
    cursor.execute(q4,(users_id,))
    # DO NOT PUT A COMIT IN FUNCTION. We only create a new cart for a user, when a new user is created, or if the users previous cart has been used for a sale.
    # The comit will occur within those functions!

def create_user(input_name, input_email, input_password):
    # Hash the password
    input_password = hash_password(input_password).decode('utf-8')  # Decode to store as string

    # SQL Queries
    insert_user_query = """
        INSERT INTO users (users_name, users_email, users_password)
        VALUES (%s, %s, %s);
    """
    
    select_user_id_query = """
        SELECT users_id FROM users WHERE users_email = %s;
    """

    try:
        # Start transaction
        cursor.execute("START TRANSACTION;")
        
        # Insert new user and handle duplicate emails
        cursor.execute(insert_user_query, (input_name, input_email, input_password))
        
        # Retrieve the new user's ID
        cursor.execute(select_user_id_query, (input_email,))
        result = cursor.fetchone()
        
        if not result:
            raise ValueError("Account creation failed: EMAIL IN USE. Please login.")
        
        current_users_id = result[0]
        
        # Create a cart for the new user
        create_cart_for_user(current_users_id)
        
        # Commit the transaction
        mydb.commit()

        return current_users_id  # Optionally use this for automatic login
        
    except Exception as e:
        print(f"Error: {e}")
        return None



def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)#turns the password into binary and then compares it with the hashed password

def u_login(email, password):
    EMAIL_QUERY = "SELECT users_id, users_name, users_password FROM users WHERE users_email = %s;"

    try:
        # fetch details
        cursor.execute(EMAIL_QUERY, (email,))
        result = cursor.fetchone()
        if result:
            users_id, users_name, stored_hashed_password = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                return jsonify({
                    "success": True,
                    "message": "Login successful!",
                    "user_id": users_id,
                    "user_name": users_name  
                })
            else:

                return jsonify({"success": False, "message": "Invalid password."})
        else:

            return jsonify({"success": False, "message": ERROR_EMAIL_NOTFOUND % email})

    except Exception as e:

        print(f"Error in u_login: {e}")
        return jsonify({"success": False, "message": "An error occurred during login."})

#login and register

def authenticate_user(data):
    email = data.get('email')
    password = data.get('password')
    is_registering = data.get('isRegistering', False)  # register flag

    if is_registering:
        # Register new user
        name = data.get('name', 'New User')
        user_id = create_user(name, email, password)
        if user_id:
            return jsonify({"success": True, "message": "Registration successful!", "user_id": user_id})
        else:
            return jsonify({"success": False, "message": "Registration failed, email might be in use."})
    else:
        # Log in existing user
        return u_login(email, password)

    
# ======================= Admin Functionalities ==========================

#adds a x amount of stock to a product - allocated by its id
def add_x_to_product_stock(x,product_id):
    GET_CURR_STOCK_QUERY = f'select stock from product where product_id = {product_id};'
    try:
        cursor.execute(GET_CURR_STOCK_QUERY)
        curr_stock = cursor.fetchone()[0]
    except:
        print("Failed to update value, please double check passed product_id")
    
    updated_stock = curr_stock + x
    QUERY = f'''
    update product 
    set stock = {updated_stock}
    where product_id = {product_id}
    '''
    try:
        cursor.execute(QUERY)
    except:
        print("Addition statement failed! Reference database if issue persists")

    return updated_stock

#removes a n amount of stock from a product
def remove_x_from_product_stock():
    return 0

def add_new_product():
    return 0
# ======================= Sale Functionalities ==========================



