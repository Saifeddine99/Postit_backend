import os
from flask import Flask
from flask_cors import CORS

from .db_models import db
DB_NAME = "database.db"
DB_PATH = os.path.join(os.getcwd(), "instance", DB_NAME)


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'hrjgvoegregfnkbguietgbget'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) # Initialize the db with the app
    
    with app.app_context(): # Create the tables if they don't exist
        db.create_all()

    from .auth import auth_bp
    from .home_page import home_page_bp
    from .post_generation import gen_post_bp
    
    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth') # Register the auth blueprint
    app.register_blueprint(home_page_bp, url_prefix='/home') # Register the home_page blueprint
    app.register_blueprint(gen_post_bp, url_prefix='/generate_post/') # Register the post generation blueprint

    return app