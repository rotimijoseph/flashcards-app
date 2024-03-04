from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from app.forms import RegisterForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST']) # methods needed for forms
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home')) # to make sure logged in users can't login in or register again
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstname=form.firstname.data, surname=form.surname.data, password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
            flash(f'Account has been created, {form.username.data}. Login to continue.', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            if User.query.filter_by(username=form.username.data).first():
                form.username.errors.append('This username is already taken. Please choose another.')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)  # remember=form.remember.data
            next_page = request.args.get('next') # args is a dictionary, next parameter is optional
            return redirect(next_page) if next_page else redirect(url_for('home')) # a ternary(?) conditional 
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form) # next pass titles in 

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html')