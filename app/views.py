from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from app.forms import RegisterForm, LoginForm, FlashCardForm, SelectSetForm
from app.models import User, FlashCard
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError
import random

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
            flash('You have successfully logged in.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home')) # a ternary(?) conditional - functionality not quite working 
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

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = FlashCardForm()
    if form.validate_on_submit():
        if request.form['action'] == 'add_flashcard':
            new_flashcard = FlashCard(set_name=form.set_name.data, question=form.question.data, answer=form.answer.data, user_id=current_user.user_id)
            db.session.add(new_flashcard)
            try:
                db.session.commit()
                flash('Added to set', 'success')
                return redirect(url_for('create'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'Error: {str(e)}', 'error')
        elif request.form['action'] == 'view_set':

            return redirect(url_for('view_set'))
    return render_template('create.html', form=form, title="New Set")

@app.route("/view_set", methods=['GET', 'POST'])
@login_required
def view_set():
    form = SelectSetForm()
    form.set.choices = [(set_name[0], set_name[0]) for set_name in get_all_set_names()]
    flashcards = []
    if form.validate_on_submit():
        set_name = form.set.data
        # get flashcards by user
        flashcards = FlashCard.query.filter_by(set_name=set_name, user_id=current_user.user_id).all()
    return render_template('view_set.html', form=form, flashcards=flashcards)

def get_all_set_names():
    return FlashCard.query.with_entities(FlashCard.set_name).distinct().all()

def get_flashcards_by_set_name(set_name):
    return FlashCard.query.filter_by(set_name=set_name).all()

@app.route("/test_memory", methods=['GET', 'POST'])
@login_required
def test_memory():
    form = SelectSetForm()
    form.set.choices = [(set_name[0], set_name[0]) for set_name in get_all_set_names()]
    flashcard = None # start with no flashcard 
    if form.validate_on_submit():
        set_name = form.set.data
        flashcards = FlashCard.query.filter_by(set_name=set_name, user_id=current_user.user_id).all()
        if flashcards:
            flashcard = random.choice(flashcards)
    return render_template('test_memory.html', form=form, flashcard=flashcard)

@app.route("/flip", methods=['POST'])
@login_required
def flip_flashcard():
    flashcard_id = request.form.get('flashcard_id')
    flashcard = FlashCard.query.get(flashcard_id)
    return render_template('test_memory.html', flashcard=flashcard, flipped=True)

@app.route("/next", methods=['POST'])
@login_required
def next_flashcard():
    # Logic to fetch the next flashcard
    # This could involve querying the database for the next flashcard
    # or maintaining a list of flashcards in the session
    # and updating the current flashcard index to get the next one
    return redirect(url_for('test_memory'))