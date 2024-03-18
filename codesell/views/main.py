from flask import Flask, session, render_template, Blueprint
#from . import bp

print('index')

bp = Blueprint('main', __name__, url_prefix = '/')

@bp.route('/')
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('index.html', username=username)
