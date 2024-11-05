from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from modules import app, db, lm
from modules.forms import ExampleForm, LoginForm
from modules.models import User


# === User login methods === 

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(email):
    if email not in User:
        return 

    user = User()
    user.email = email
    return User.query.get(int(id))

# === Cart Functions ===

def add_to_cart(product_id , user_id):
    user = user_id
    product = Product.query.filter(Product.id == product_id)
    cart_item = Cart(product=product , )
    db.session.add(cart_item)
    db.session.commit()

    return 