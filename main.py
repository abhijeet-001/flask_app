# Import Packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_googlemaps import GoogleMaps

# Define app
app = Flask(__name__)

# Setting App configuration
app.config.from_pyfile("settings.py")

# Setting up db
db = SQLAlchemy(app)

# Setting up csrf
csrf = CSRFProtect(app)

# Setting up login manager
login_manager = LoginManager(app)
# Set Admin Login URL for redirection
login_manager.login_view = 'admin_login'

# Initializing Google App
GoogleMaps(app)


# Import views
from views import *
from models import Request, Admin
from cli import *

if __name__ == "__main__":
    app.run()