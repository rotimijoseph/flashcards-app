from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class RegisterForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def __repr__(self):
        return f"user('{self.username}',  '{self.firstname}', '{self.surname}')"

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class FlashCardForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    next = SubmitField('Next')