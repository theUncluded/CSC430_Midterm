from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm
from app.forms import ExampleForm, LoginForm
from app.models import User

#Home Page
@app.route('/') 
def index():
	return render_template('index.html')

@app.route('/admin/')
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
