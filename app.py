from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import os

print("Template Folder Path:", os.path.join(os.getcwd(), "templates"))

app = Flask(__name__, static_folder='static')


# Load .env file
load_dotenv()

# Access environment variables
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://Bimla-Asus\\SQLEXPRESS/GlassSlipperBridal?driver=ODBC+Driver+17+for+SQL+Server"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(debug=True)

