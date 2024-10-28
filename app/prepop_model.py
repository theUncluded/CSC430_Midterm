from app import db

#use this if we are using a pre-populated table

with app.app_context():
    db.reflect()

# From the default bind key
class Product(db.Model):
    __table__ = db.metadata.tables["Product"]

class Product_Cart(db.Model):
    __table__ = db.metadata.tables["Cart"]

# From an "auth" bind key
class User(db.Model):
    __table__ = db.metadatas["auth"].tables["User"]

class Product_Cart(db.Model):
    __table__ = db.metadatas["auth"].tables["Product_Cart"]

class Sales_History(db.Model):
    __table__ = db.metadatas["auth"].tables["Sales_History"]