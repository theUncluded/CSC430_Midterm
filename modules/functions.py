import mysql.connector
import bcrypt

from flask import render_template, request, jsonify, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# =======================SQL ACTIONS=======================

mydb = mysql.connector.connect(#could potentially make this configurable with global vars
    host = "localhost",
    user = "root",
    password = "1234",
    database = "csc430"
)
cursor = mydb.cursor()

def hash_password(password):
    salt = bcrypt.gensalt()#generates a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)# Hashs the password with the salt after converting it into binary
    return hashed_password #returns the now hased password


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)#turns the password into binary and then compares it with the hashed password


def create_user(input_name,input_email,input_password):
    input_password = hash_password(input_password) #hash our example password
    users_data = (input_name,input_email,input_password)
    q1 = "insert into users (users_name,users_email,users_password)values (%s,%s,%s);" #list of sql queries we are using
    q2 = "select users_id from users where users_email = %s;"
    q3 = "insert into cart (users_id) values (%s);"
    q4 = "update users set current_cart_id = (select max(cart_id) from cart where cart.users_id = users.users_id) where users_id = %s;"
    cursor.execute("start transaction;")
    cursor.execute(q1,(users_data))
    cursor.execute(q2,(input_email,))
    result = cursor.fetchall() #should always return only 1 row
    for row in result:
        users_id = row
        current_users_id = users_id[0] #user id to store in session (will be returned by function if we want to automatically log someone in to the account they created.)
    cursor.execute(q3,(current_users_id,))
    cursor.execute(q4,(current_users_id,))
    mydb.commit()
    return current_users_id
# test function to fill connected db with dummy data
def user_test_db_fill():
    user_id = create_user("Rich","Rich'sbadpassword","Rich2@exampleemail.com")#user name email password
    print (user_id)#debug print

#call to close connection to db
def close_conn_2_db():
    cursor.close()
    mydb.close() 

def pull_product_list():
    QUERY = "select * from product"
    cursor.execute(QUERY)
    result = cursor.fetchall()
    print(result) #debug , comment when finished
    return jsonify(result)


