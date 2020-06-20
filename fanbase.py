from app import app, db
from app.models import User, Portfolio, Team, Post, ShortTeam

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Portfolio': Portfolio, 'Team': Team, 'Post': Post, 'ShortTeam': ShortTeam}
