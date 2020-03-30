from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Portfolio
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
import xlrd

@app.route('/')
@app.route('/index')
@login_required
def index():
    excelfile = 'teamprices.xlsx'
    wb = xlrd.open_workbook(excelfile)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    teamslist = []
    for i in range(31): 
        teams = sheet.cell_value(i, 0)
        prices = str(sheet.cell_value(i, 17))
        teamslist.append(teams + " : " + "$" + prices)

    return render_template('index.html', title='Home', teamslist = teamslist)

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
