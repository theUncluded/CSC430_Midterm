from app import db
# This is the database model code to instantiate a db with the following columns, keys, and so forth
# If we decide to move to a pre-populated database, refer to prepop_model.py
class Product(db.Model):
	product_id = db.Column(db.Integer, primary_key = True)
	product_name = db.Column(db.String(100))
	product_price = db.Column(db.double(10,2))
	product_stock = db.Column(db.Integer)

class Cart(db.Model):
    cart_id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey(User.user_id))

class Product_Cart(db.Model):
    cart_id = db.Column(db.Integer, db.ForeignKey(Cart.cart_id) , unique = True)
    product_id = db.Column(db.Integer , db.ForeignKey(Product.product_id))
    product_quantity = db.Column(db.Integer)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(500), unique = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique = True)
    address = db.Column(db.String(255))
    card_number = db.Column(db.String(16), unique = True)
    card_cvv = db.Column(db.String(3))
    privledge = db.Column(db.Integer)

    def is_privledged(self):
        if self.privledge > 0:
            return True
        
        return False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
class Sales_History(db.Model):
    sale_id = db.Column(db.Integer , primary_key = True)
    cart_id = db.Column(db.Integer , db.ForeignKey(Cart.cart_id))
    date_time = db.Column(db.date_time)
    sale_total = db.Column(db.double(10,2))

#With all tables defined call create_db to create the table schema in a db
#IF models are defined in other modules, sqlalch will NOT know about them
with app.app_context():
    db.create_all()