from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class AdviceForm(FlaskForm):
    interest = SelectField('Interest', choices=[], validators=[DataRequired()])
    text = TextAreaField('Advice Text', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Advice')

class InterestForm(FlaskForm):
    name = StringField('New Interest', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Interest')

class RatingForm(FlaskForm):
    advice_id = IntegerField('Advice ID', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Rate')
