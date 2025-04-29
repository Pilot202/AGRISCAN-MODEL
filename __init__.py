# app/__init__.py

# Import common dependencies
from flask import Flask

# Create a Flask app instance (if applicable)
app = Flask(__name__)

# Import routes or other modules
from app.routes import auth, image_processing, user
