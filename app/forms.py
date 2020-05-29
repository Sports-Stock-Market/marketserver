from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Portfolio, Team, Post

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class BuyForm(FlaskForm):
    buy = SelectField('Teams', coerce=float, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Purchase')

class SellForm(FlaskForm):
    sell = SelectField('Teams', coerce=float, validators = [DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Sell')

class PostForm(FlaskForm):
    team = SelectField('Team', coerce=str, validators = [DataRequired()])
    price = FloatField('Price / Share', validators = [DataRequired()])
    quantity = IntegerField('Quantity', validators = [DataRequired()])
    submit = SubmitField('Post')

class PurchaseForm(FlaskForm):
    submit = SubmitField('Purchase')

class RevokeForm(FlaskForm):
    submit = SubmitField('Revoke Offer')
