from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_cors import CORS
from flask_admin import Admin
from dotenv import load_dotenv
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint
import os

load_dotenv()

db = SQLAlchemy()
DB_NAME = "FlyerScanApp.sqlite"

app = Flask(__name__)

def create_app():
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['FLASK_ADMIN_SWATCH'] = 'united'

    db.init_app(app)

    from .views import views
    from .auth import auth
    github_blueprint = make_github_blueprint(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'))
    google_blueprint = make_google_blueprint(client_id=os.getenv('GOOGLE_CLIENT_ID'), client_secret=os.getenv('GOOGLE_CLIENT_SECRET'), 
                                            redirect_url='/login/google',
                                            scope=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",'openid'],
                                            authorized_url='/google/authorized'
                                            )
                                                                 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(github_blueprint, url_prefix='/github_login')
    app.register_blueprint(google_blueprint, url_prefix='')

    from .models import Users

    from .admin import appnamey
    appnamey(app)

    create_database(app)

    CORS(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            from .admin import superuserNewDB
            superuserNewDB(app)
    
        print('Created Database!')