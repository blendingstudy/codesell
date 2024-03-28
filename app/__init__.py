from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    """ from app.models.user import User
    from app.models.product import Product
    from app.models.cart import Cart
    from app.models.order import Order
    from app.models.funding import Funding

    from app.controllers.auth_controller import auth_bp
    from app.controllers.product_controller import product_bp
    from app.controllers.cart_controller import cart_bp
    from app.controllers.order_controller import order_bp
    from app.controllers.funding_controller import funding_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(funding_bp) """

    return app