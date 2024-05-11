from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
   app = Flask(__name__)
   app.config.from_object(Config)

   db.init_app(app)
   migrate.init_app(app, db)
   login_manager.init_app(app)

   @login_manager.user_loader
   def load_user(user_id):
       return User.query.get(int(user_id))

   @app.route('/')
   def index():
       return render_template('index.html')

   from app.models.user import User
   from app.models.category import Category
   from app.models.product import Product
   from app.models.cart import Cart
   from app.models.order import Order
   from app.models.funding import Funding
   from app.models.review import Review

   from app.controllers.auth_controller import auth_bp
   from app.controllers.product_controller import product_bp
   from app.controllers.cart_controller import cart_bp
   from app.controllers.order_controller import order_bp
   from app.controllers.funding_controller import funding_bp
   from app.controllers.mypage_controller import mypage_bp
   from app.controllers.admin_controller import admin_bp
   from app.controllers.review_controller import review_bp

   app.register_blueprint(auth_bp)
   app.register_blueprint(product_bp)
   app.register_blueprint(cart_bp)
   app.register_blueprint(order_bp)
   app.register_blueprint(funding_bp)
   app.register_blueprint(mypage_bp)
   app.register_blueprint(admin_bp)
   app.register_blueprint(review_bp)

   return app