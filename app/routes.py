from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, ListForm, DeleteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Item
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required

def index():
	user = {'username': 'Ben'}
	form = ListForm()
	deleteform = DeleteForm()
	items = Item.query.filter_by(user_id=current_user.id).order_by("due")

	# on click, adds action to db
	if form.validate_on_submit():	
			action = Item(body=form.action.data, due = form.due.data, user_id=current_user.id)
			db.session.add(action)
			db.session.commit()

	# deletes actions from db
	if deleteform.validate_on_submit():
		if request.method == 'POST':
			ids = request.form.getlist('checkbox')
			print(request.form.getlist('checkbox'))
			intids = [int(x) for x in ids]
			print(intids)
			x = 0
			while x < len(intids):
				deleting = Item.query.filter_by(id = intids[x]).first()
				db.session.delete(deleting)
				x = x + 1
			
			db.session.commit()


	return render_template('index.html', title='List', form=form, items = items, deleteform = deleteform)

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
