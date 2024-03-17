from flask import Flask, session, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    #from . import models

    from views import bp, auth_bp
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)
    #app.register_blueprint(product_bp)
    #app.register_blueprint(cart_bp)
    #app.register_blueprint(funding_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
