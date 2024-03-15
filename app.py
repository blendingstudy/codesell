from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from views.auth import auth_bp #, product_bp, cart_bp, funding_bp
from models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(auth_bp)
#app.register_blueprint(product_bp)
#app.register_blueprint(cart_bp)
#app.register_blueprint(funding_bp)

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('index.html', username=username)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('db')
    app.run(debug=False)