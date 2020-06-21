from flask import Flask, jsonify, render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, BuyForm, SellForm, PostForm, PurchaseForm, RevokeForm, SearchForm, ShortForm, BuybackForm, SetForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Portfolio, Team, Post, ShortTeam
from flask_login import login_required
from flask import request, g
from werkzeug.urls import url_parse
from teamprices import teamprices
from sqlalchemy.sql import exists, operators
from datetime import datetime
import threading
import click
from flask.cli import with_appcontext
#import time, webbrowser

'''def buyAt():
    threading.Timer(5.0, buyAt).start()
    teams = Team.query.all()
    teamprices.update(teamprices)
    for name, price in teamprices.items():
        for t in teams:
            port = Portfolio.query.filter_by(id = t.portfolio_id).first()
            if t.team == name:
                if t.buy_at is None or t.buy_quant is None or t.buy_quant == 0:
                    pass

                elif (price * t.buy_quant) > port.money:
                    print("low funds")

                else:
                    print(price)
                    print(t.buy_at)
                    if t.buy_at >= price:
                        print('acquiring team')
                        t.num_team += t.buy_quant
                        port.money -= (price * t.buy_quant)
                        t.buy_quant = 0
                        db.session.commit()
#buyAt()'''

@click.command(name = "create_tables")
@with_appcontext
def create_tables():
    db.create_all()

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

    ''' WHERE DO I RUN THIS'''
    port = Portfolio.query.filter_by(user_id = current_user.id).first()
    short_teams = ShortTeam.query.filter_by(portfolio_id = port.id).all()


    for team in short_teams:
        if team.timestamp.date() >= datetime.today().date():
            for name, price in teamprices.items():
                if team.team == name:
                    new_price = price
                    new_money = (team.price - new_price)
                    print(new_money)
                    port.money = port.money + new_money
                    team.num_team = 0

    ''' '''

    teamssssss = [(price, name) for name, price in teamprices.items()]
    #print(teamssssss)

    form = BuyForm()
    form.buy.choices = teamssssss


    if form.validate_on_submit():
        money = port.money
        #print(money)
        price = form.quantity.data * form.buy.data


        def getName():
            for name, price in teamprices.items():
                if form.buy.data == price:
                    print(name)
                    return name
        teams = getName()

        team = Team.query.filter_by(portfolio_id = port.id, team = teams).first()

        if port.money - price < 0:
            flash('tough luck buttercup, you need more fans')

        elif form.quantity.data <= 0:
            flash('ILLEGAL MOVE')
        

        elif team != None:
            flash('buyers beware')
            new_money = port.money = (money - price)
            #team = Team.query.filter_by(portfolio_id = portfolio.id()).first()
            team.num_team = team.num_team + form.quantity.data

            db.session.add(port)
            db.session.add(team)

        else:
            flash('buyers beware')
            new_money = port.money = (money - price)
            
            teams = getName()
            print(teams)
            team = Team(team = teams, num_team = form.quantity.data, portfolio_id = port.id, price = form.buy.data)

            db.session.add(port)
            db.session.add(team)
    
    
    db.session.commit()

    return render_template('index.html', title='Home', form = form)


@app.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    port = Portfolio.query.filter_by(user_id = current_user.id).first()
    money = port.money

    teams = Team.query.filter(Team.num_team != 0, Team.portfolio_id == port.id).all()


    for team in teams:
        for name, price in teamprices.items():
            if team.team == name:
                team.price = price
    

    short_teams = ShortTeam.query.filter_by(portfolio_id = port.id).all()
    print(short_teams)


    form = SellForm()
    form.sell.choices = [(t.price, t.team) for t in Team.query.filter(Team.num_team != 0, Team.portfolio_id == port.id)]

    if form.validate_on_submit():
        def getName():
                for name, price in teamprices.items():
                    if form.sell.data == price:
                        print(name)
                        return name
        name = getName()

        port = Portfolio.query.filter_by(user_id = current_user.id).first()
        team = Team.query.filter_by(team = name, portfolio_id = port.id).first()
        money = port.money
        price = form.quantity.data * form.sell.data

        if form.quantity.data > team.num_team:
            flash('sell you cannot if have you do not')

        elif form.quantity.data <= 0:
            flash('ILLEGAL MOVE')

        else:
            flash('The trends are your friends')
            port.money = (money + price)
            team.num_team = (team.num_team - form.quantity.data)
            db.session.commit()
            return redirect(url_for('portfolio'))

    
    buy_back_form = BuybackForm()

    if buy_back_form.validate_on_submit():
        if request.method == 'POST':
            team_id = request.form.get('radiobutt')
            print(team_id)

            if team_id is None:
                flash('Select a team')

            else:
                team = ShortTeam.query.filter_by(id = team_id).first()
                for name, price in teamprices.items():
                    if team.team == name:
                        new_price = price
                        new_money = (team.price - new_price)
                        print(new_money)
                        port.money = port.money + (new_money * team.num_team)
                        db.session.delete(team)
                        db.session.commit()
                        return redirect(url_for('portfolio'))
    




    return render_template('portfolio.html', title='Portfolio', form = form, money = money, teams = teams, short_teams = short_teams, buy_back_form = buy_back_form)

@app.route('/short', methods=['GET', 'POST'])
@login_required
def short():
    port = Portfolio.query.filter_by(user_id = current_user.id).first()
    
    teamssssss = [(price, name) for name, price in teamprices.items()]

    form = ShortForm()
    form.short.choices = teamssssss

    def getName():
        for name, price in teamprices.items():
            if form.short.data == price:
                print(name)
                return name
        
    teams = getName()
    print(teams)

    if form.validate_on_submit():
        days = form.exp_date.data - datetime.today().date()
        #print(days.days)
        if form.exp_date.data <= datetime.today().date():
            flash('unless you have a time machine, you need to pick a date after today')

        elif port.money < form.quantity.data:
            flash('The shorting fee is higher than you can afford')

        elif form.quantity.data <= 0:
            flash('ILLEGAL MOVE')
        
        else:
            flash('no risk, no reward')
            print(form.quantity.data * days.days)
            port.money = (port.money - (form.quantity.data))
            short_team = ShortTeam(team = teams, num_team = form.quantity.data, timestamp = form.exp_date.data, portfolio_id = port.id, price = form.short.data)
            db.session.add(short_team)
            db.session.commit()
            return redirect(url_for('portfolio'))

        

    return render_template('short.html', title='Short', form = form)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    port = Portfolio.query.filter_by(user_id = current_user.id).first()
    money = port.money
    teams = Team.query.filter(Team.num_team != 0, Team.portfolio_id == port.id).all()
    form = PostForm()
    form.team.choices = [(t.team, t.team) for t in Team.query.filter(Team.num_team != 0, Team.portfolio_id == port.id)]

    team = Team.query.filter_by(team = form.team.data, portfolio_id = port.id).first()

    if form.validate_on_submit():
        if form.quantity.data > team.num_team:
            flash('sell you cannot if have you do not')

        elif form.quantity.data <= 0:
            flash('ILLEGAL MOVE')

        else:
            flash('It is a market of stocks, not a stock market')
            post = Post(team = form.team.data, price = (form.price.data * form.quantity.data), num_team = form.quantity.data, user_id = current_user.id)
            team.num_team = team.num_team - form.quantity.data
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('marketplace'))


    return render_template('post.html', title = 'Post', form = form, money = money, teams = teams)

@app.route('/marketplace', methods=['GET', 'POST'])
@login_required
def marketplace():
    posts = Post.query.order_by(Post.timestamp.desc()).all()

    form = PurchaseForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            post_id = request.form.get('mycheckbox')
            print(request.form.get('mycheckbox'))

            if post_id is None:
                flash('Select an Offer')



            else:
                post = Post.query.filter_by(id = post_id).first()

                port_seller = Portfolio.query.filter_by(user_id = post.user_id).first()
                port_buyer = Portfolio.query.filter_by(user_id = current_user.id).first()

                #print(db.session.query(Team.id).filter_by(team = post.team).scalar())

                team = Team.query.filter_by(portfolio_id = port_buyer.id, team = post.team).first()

                if team is None:
                    def getPrice():
                        for name, price in teamprices.items():
                            if post.team == name:
                                return price

                    price = getPrice()
                    add_team = Team(team = post.team, num_team = post.num_team, price = price, portfolio_id = port_buyer.id)


                    db.session.add(add_team)
                    db.session.commit()


                teams = Team.query.filter_by(portfolio_id = port_buyer.id, team = post.team).first()

                if (port_buyer.user_id == port_seller.user_id):
                    flash('you cannot buy your own offer')

                elif (port_buyer.money - post.price) < 0:
                    flash('buy you cannot if have you do not')
                else:
                    flash('When the tide goes out, you see who is swimming naked')
                    print(post.price)
                    lost_money = (port_buyer.money - post.price)
                    port_buyer.money = lost_money
                    gained_money = (port_seller.money + post.price)
                    port_seller.money = gained_money
                    
                    teams.num_team = post.num_team + teams.num_team

                    delete_post = post
                    db.session.delete(delete_post)

                    db.session.commit()
                    return redirect(url_for('portfolio'))
    
    return render_template('marketplace.html', title = 'Marketplace', posts = posts, form = form)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    post = Post.query.all()
    teamssssss = [(name, name) for name, price in teamprices.items()]
    #print(teamssssss)

    form = SearchForm()
    form.search_team.choices = teamssssss

    
    search_results = Post.query.filter_by(team = form.search_team.data).order_by((Post.price)).all()

    if form.validate_on_submit():
        if not search_results:
            flash('No posts for that team, try a new team or purchase from the computer')

    buy_form = PurchaseForm()

    if buy_form.validate_on_submit():
        if request.method == 'POST':
            post_id = request.form.get('post')
            print(request.form.get('post'))

            if post_id is None:
                flash('Select an Offer')

            else:
                post = Post.query.filter_by(id = post_id).first()

                port_seller = Portfolio.query.filter_by(user_id = post.user_id).first()
                port_buyer = Portfolio.query.filter_by(user_id = current_user.id).first()

                #print(db.session.query(Team.id).filter_by(team = post.team).scalar())

                team = Team.query.filter_by(portfolio_id = port_buyer.id, team = post.team).first()

                if team is None:
                    def getPrice():
                        for name, price in teamprices.items():
                            if post.team == name:
                                return price

                    price = getPrice()

                    add_team = Team(team = post.team, num_team = post.num_team, price = price, portfolio_id = port_buyer.id)

                    db.session.add(add_team)
                    db.session.commit()


                teams = Team.query.filter_by(portfolio_id = port_buyer.id, team = post.team).first()

                if (port_buyer.user_id == port_seller.user_id):
                    flash('you cannot buy your own offer')

                elif (port_buyer.money - post.price) < 0:
                    flash('buy you cannot if have you do not')
                else:
                    flash('When the tide goes out, you see who is swimming naked')
                    lost_money = (port_buyer.money - post.price)
                    gained_money = (port_seller.money + post.price)
                    port_buyer.money = lost_money
                    port_seller.money = gained_money
                    teams.num_team = post.num_team

                    delete_post = post
                    db.session.delete(delete_post)

                    db.session.commit()
                    return redirect(url_for('portfolio'))



    return render_template('search.html', title = 'Search', form = form, search_results = search_results, post = post, buy_form = buy_form)

@app.route('/rankings', methods=['GET', 'POST'])
@login_required
def rankings():
    users = User.query.all()
    ports = Portfolio.query.all()
    def getAssests(p):
            assets = p.money
            teams = Team.query.filter_by(portfolio_id = p.id).all()
            for t in teams:
                assets = assets + (t.price * t.num_team)

            return(assets)
            #return jsonify(result = assets)
    

    for p in ports:
        for u in users:
            if p.user_id == u.id:
                u.total_assets = getAssests(p)
                print(u.total_assets)

    user = User.query.order_by(User.total_assets.desc())



    return render_template('rankings.html', title = 'Rankings', ports = ports, user = user)


@app.route('/prices', methods=['GET', 'POST'])
@login_required
def prices():
    port = Portfolio.query.filter_by(user_id = current_user.id).first()
    team_prices = [(name, price) for name, price in teamprices.items()]
    form = SetForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            team = request.form.get('set')
            print(request.form.get('set'))

            if team is None:
                flash('Select a team')
            
            else:
                flash('set')
                team_set = Team.query.filter_by(team = team, portfolio_id = port.id).first()
                print(team_set.team)
                team_set.buy_at = form.buy.data
                team_set.buy_quant = form.quantity.data
                db.session.commit()



    return render_template('prices.html', title = 'Team Prices', form = form, team_prices = team_prices)




@app.route('/myposts', methods=['GET', 'POST'])
@login_required
def myposts():
    form = RevokeForm()
    posts = Post.query.filter_by(user_id = current_user.id)
    port = Portfolio.query.filter_by(user_id = current_user.id).first()

    if form.validate_on_submit():
        if request.method == 'POST':
            post_id = request.form.get('mycheckbox')
            print(request.form.get('mycheckbox'))

            if post_id is None:
                flash('Select an Offer')

            else:
                flash('Bulls make money, bears make money, pigs get slaughtered')

                post = Post.query.filter_by(id = post_id).first()
                team = Team.query.filter_by(portfolio_id = port.id, team = post.team).first()

                team.num_team = (team.num_team + post.num_team)



                db.session.delete(post)
                db.session.commit()


    return render_template('myposts.html', title = 'My Offers', form = form, posts=posts)



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
        db.session.flush()
        print(user.id)
        portfolio = Portfolio(user_id = user.id)
        db.session.add(portfolio)
        db.session.flush()
        print(portfolio.id)
        for name, price in teamprices.items():
            team = Team(team = name, num_team = 0, price = price, portfolio_id = portfolio.id)
            db.session.add(team)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
