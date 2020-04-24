from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, BuyForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Portfolio, Teams
from flask_login import login_required
from flask import request, g
from werkzeug.urls import url_parse
import xlrd
import sqlalchemy

@app.before_request
def global_user():
    g.user = current_user

# Make current user available on templates
@app.context_processor
def template_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}
        

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required 
def index():
    cash = db.session.query(Portfolio.cash).filter_by(user_id=current_user.id).first()
    excelfile = 'prices.xlsx'
    wb = xlrd.open_workbook(excelfile)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    teampricelist = []
    teamslist = []
    priceslist = []
    for i in range(1, 31):
        teams = sheet.cell_value(i, 0)
        prices = str(sheet.cell_value(i, 17))
        teamslist.append(teams)
        priceslist.append(prices)
        teampricelist.append(teams + " : " + "$" + prices)


    all_teamprice = db.session.query(Teams).all()
    all_teams = db.session.query(Teams.all_teams)
    price = db.session.query(Teams.price)





    teamssssss = [(i.price, i.all_teams) for i in all_teamprice]
    
    form = BuyForm()
    form.buy.choices = teamssssss


    if form.validate_on_submit():
        flash('buyers beware')
        price = form.quantity.data * form.buy.data
        print(form.quantity.data)
        print(form.buy.data)
        print(price)
        new_cash = Portfolio(cash = (cash - price))
        print(new_cash)
        db.session.append(new_cash)

    return render_template('index.html', title='Home',teampricelist = teampricelist, form = form)

# logs users in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
# logs them out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
# code for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
