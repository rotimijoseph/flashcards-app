from flask import render_template, redirect, url_for, flash
from app import app, db, bcrypt
from app.forms import RegisterForm
from app.models import User

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST']) # methods needed for forms
def register():
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
                form.username.errors.append('This username is already taken. Please choose another')
    return render_template('register.html', form=form)

@app.route("/login")
def login():
    return render_template('login.html')