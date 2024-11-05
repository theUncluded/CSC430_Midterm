from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, jsonify, redirect
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from modules import functions , config, model

app = Flask('csc430')  
db = SQLAlchemy() #flask-sqlalchemy
#Configuration of application, errors with config file lead to hard coding config in app
#Fix soon
e_string = model.ENGINE_STRING
print(e_string)
app.config["SQLALCHEMY_DATABASE_URI"] = e_string
db.init_app(app)

# =======================LOGIN MANAGER INIT=======================
lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

# ===Main & Admin Pages===
@app.route('/') 
def index():
	return render_template('index.html')
#pull product list uses functions library found in app dir to return a json of the product list in full
def index2():
    return functions.pull_product_list()

@app.route('/admin/')
def admin_panel():
    return render_template('admin_panel.html')

# ===User Login Pages===

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

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080)