from app import db,login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import xlrd

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teams = db.Column(db.String(140)) # possibly a foreign key to another Teams class
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cash = db.Column(db.Integer, default=10000)

    def __repr__(self):
        return '<Portfolio {}>'.format(self.user_id)

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    all_teams = db.Column(db.String(140))
    price = db.Column(db.Float)

    def __repr__(self):
        return '<Teams {}>'.format(self.all_teams)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def add_teamprice():
    excelfile = 'prices.xlsx'
    wb = xlrd.open_workbook(excelfile)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    teampricelist = []
    teamslist = []
    priceslist = []
    for i in range(1, 31):
        teams = sheet.cell_value(i, 0)
        prices = (sheet.cell_value(i, 17))
        teamslist.append(teams)
        priceslist.append(prices)
        all_teamsandprices = Teams(all_teams = teams, price = prices)
        db.session.add(all_teamsandprices)

    db.session.commit()

def delete_teamprice():
    deleting = Teams.query.first()
    #all_teams = db.session.query(Teams.all_teams)
    #price = db.session.query(Teams.price)
    db.session.delete(deleting)
    db.session.commit()

# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
# delete_teamprice()
#
# add_teamprice()
