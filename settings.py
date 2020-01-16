# Secret Key
SECRET_KEY = "YOUR_SECRET_KEY"

# Defines App's mode 
# True or False
DEBUG = False

# Database Credentials
DB_USER = "YOUR_DB_USER"
DB_PASSWORD = "YOUR_DB_PASSWORD"
HOST = "YOUR_DB_HOST"
DB_NAME = "YOUR_DB_NAME"

# SQLAlchemy Database URL
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://"+DB_USER+":"+DB_PASSWORD+"@"+HOST+"/"+DB_NAME

# Set Warning to False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Google Map API Key
GOOGLEMAPS_KEY = 'YOUR_GOOGLEMAPS_KEY'

# Ipinfo Token
IPINFO_TOKEN = 'YOUR_IPINFO_TOKEN'
