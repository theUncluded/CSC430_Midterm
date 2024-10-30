from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import ExampleForm, LoginForm
from app.models import User

#Home Page
@app.route('/') 
def index():
	return render_template('index.html')

def index2():
    products_db = Product.query.

    #Debug statement, comment out for demo
    with engine.connect() as conn:
        for row in conn.execute(products_db)
        print(row)
    
    return jsonify(products_db)

@app.route('/admin/')
@admin_only
def admin_panel():
    return render_template('admin_panel.html')


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

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(g.user)

    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

# === Cart Functions ===

def add_to_cart(product_id , user_id):
    user = user_id
    product = Product.query.filter(Product.id == product_id)
    cart_item = Cart(product=product , )
    db.session.add(cart_item)
    db.session.commit()

    return 