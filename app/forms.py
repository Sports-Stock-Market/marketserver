from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Portfolio, Team, Post, ShortTeam

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

class ShortForm(FlaskForm):
    short = SelectField('Team', coerce=float, validators = [DataRequired()])
    quantity = IntegerField('Quantity', validators = [DataRequired()])
    exp_date = DateField('Expiration Date', format = '%Y-%m-%d', validators = [DataRequired()])
    submit = SubmitField('Short')

class BuybackForm(FlaskForm):
    submit = SubmitField('buy back early')

class PurchaseForm(FlaskForm):
    submit = SubmitField('Purchase')

class RevokeForm(FlaskForm):
    submit = SubmitField('Revoke Offer')

class SetForm(FlaskForm):
    quantity = IntegerField('Quantity', validators = [DataRequired()])
    buy = FloatField('Auto Buy', validators = [DataRequired()])
    submit = SubmitField('Set')

class SearchForm(FlaskForm):
    search_team = SelectField('Pick Team Name', validators=[DataRequired()])
    submit = SubmitField('Search')
