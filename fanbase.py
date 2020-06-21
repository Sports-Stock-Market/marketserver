from app import app, db
from app.models import User, Portfolio, Team, Post, ShortTeam, Teamprice
import click
from flask.cli import with_appcontext

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Portfolio': Portfolio, 'Team': Team, 'Post': Post, 'ShortTeam': ShortTeam, 'Teamprice': Teamprice}

@click.command(name = "create_tables")
@with_appcontext
def create_tables():
    db.create_all()
