from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect # import csrf protect class (task 4)

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
app = Flask(__name__)
csrf = CSRFProtect() #(task 4)

def create_app():
    

    app.config['SECRET_KEY'] = 'secret-key-do-not-reveal'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photos.db'
    CWD = Path(os.path.dirname(__file__))
    app.config['UPLOAD_DIR'] = CWD / "uploads"

    db.init_app(app)
    csrf.init_app(app) # initialise global csrf protection (task 4)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from project.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
