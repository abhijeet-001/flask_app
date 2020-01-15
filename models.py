from datetime import datetime
from main import db, login_manager
from sqlalchemy_utils import EmailType
from flask_login import UserMixin

# Define Models

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(40))
    date_created = db.Column(db.DateTime, default=datetime.now)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType)
    password = db.Column(db.String(200), nullable=False)
    is_fresh_login = db.Column(db.Boolean, default=True )
    date_created = db.Column(db.DateTime, default=datetime.now())