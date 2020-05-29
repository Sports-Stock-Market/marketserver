from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, BuyForm, SellForm, PostForm, PurchaseForm, RevokeForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Portfolio, Team, Post
from flask_login import login_required
from flask import request, g
from werkzeug.urls import url_parse
from teamprices import teamprices
from sqlalchemy.sql import exists

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
    teamssssss = [(price, name) for name, price in teamprices.items()]
    #print(teamssssss)

    form = BuyForm()
    form.buy.choices = teamssssss


    if form.validate_on_submit():
        port = Portfolio.query.filter_by(user_id = current_user.id).first()
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
    print(port)
    money = port.money
    print(money)

    teams = Team.query.filter_by(portfolio_id = port.id).all()

    for team in teams:
        for name, price in teamprices.items():
            if team.team == name:
                team.price = price
                print(team.price)
    
    db.session.commit()

    form = SellForm()
    form.sell.choices = [(t.price, t.team) for t in Team.query.filter_by(portfolio_id = port.id)]

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
        else:
            flash('The trends are your friends')
            port.money = (money + price)
            team.num_team = (team.num_team - form.quantity.data)
            db.session.commit()
            return redirect(url_for('index'))



    return render_template('portfolio.html', title='Portfolio', form = form, money = money, teams = teams)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    port = Portfolio.query.filter_by(user_id = current_user.id).first()
    form = PostForm()
    form.team.choices = [(t.team, t.team) for t in Team.query.filter_by(portfolio_id = port.id)]

    team = Team.query.filter_by(team = form.team.data, portfolio_id = port.id).first()

    if form.validate_on_submit():
        if form.quantity.data > team.num_team:
            flash('sell you cannot if have you do not')

        else:
            flash('It is a market of stocks, not a stock market')
            post = Post(team = form.team.data, price = (form.price.data * form.quantity.data), num_team = form.quantity.data, user_id = current_user.id)
            team.num_team = team.num_team - form.quantity.data
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('marketplace'))


    return render_template('post.html', title = 'Post', form = form)

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
                    lost_money = (port_buyer.money - post.price)
                    gained_money = (port_seller.money + post.price)
                    port_buyer.money = lost_money
                    port_seller.money = gained_money
                    teams.num_team = post.num_team

                    delete_post = post
                    db.session.delete(delete_post)

                    db.session.commit()
                    return redirect(url_for('portfolio'))
    
    return render_template('marketplace.html', title = 'Marketplace', posts = posts, form = form)

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
    team_prices = [(name, price) for name, price in teamprices.items()]
    return render_template('prices.html', title = 'Team Prices', team_prices = team_prices)




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
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
