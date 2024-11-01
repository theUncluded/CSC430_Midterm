import os
import sys
import pymongo
from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi


#make a connection with mongodb && test connection
def conn_to_mongo():
    uri = os.environ['MONGO_URI']
    client = MongoClient(uri , server_api=ServerApi('1'))

    #return exception if connection fails
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)

#db collection connects and defines the mongodb collection 
def db_collection_conn(collection_name):
    client = conn_to_mongo()

    #define db name and collection for specific collection to reference: cart,product,sale,product_pair,users
    DB_NAME = "csc430"
    COLL_NAME = collection_name

    MONGODB_COLLECTION = client[DB_NAME][COLL_NAME]

    return MONGODB_COLLECTION

#pull all product information from mongodb will return a jsonified product list of all product information: id,price,name,stock (NOT NEAT)
def pull_all_product():
    collection = db_collection_conn("product")

    prod_list = [] #empty dict to append products to
    for x in collection.find():
        prod_list.append(x)
        print(x)#debug
    
    return jsonify(prod_list)

#add_a_product will add a parametered product to the database
def add_a_product(p_name,p_id,p_stock,p_price):
    collection = db_collection_conn("product")
    new_product = {"product_id" : p_id , "product_name" : p_name , "price" : p_price , "stock" : p_stock}
    try:
        push_product = collection.insert_one(new_product)
        print("Product push successful")
    except Exception as e:
        print(e)

#product_sale handles an item being sold, subtracting from the sold item's stock by the quantity sold, singular function cannot do multiple products
def product_sale(p_id,quantity_sold):#p_id or product id is the id of the product that was sold, quantity sold is an int representing... the quantity sold
    collection = db_collection_conn("product")
    query = {"product_id" : p_id} 
    get_query = collection.find(query)#find product via id
    
    for key , val in get_query.items():#using the key val pair of mongo's layout, find the stock column and allocate the value to variable 'stock'
        if 'stock' in key:
            stock = val
            print(val)
    stock = stock - quantity_sold #subtract the quantity sold from stock 

    new_value = {"$set": {"stock" : stock}} #define the new value set for stock 

    collection.update_one(query,new_value) # update the original query with the new stock value

#remove_a_product removes a product row from the database via the id
def remove_a_product(p_id):
    collection = db_collection_conn("product")
    query = {"product_id" : p_id}

    try:
        collection.delete_one(query)
        print("Success")
    except Exception as e:
        print("Failure, please check the product id passed. ", e)
