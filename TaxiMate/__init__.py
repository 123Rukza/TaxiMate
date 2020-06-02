# Python package initialization file
# Imports
from flask import Flask

# Create flask object
app = Flask(__name__)

# Routes file imported after initializing flask to avoid cyclic import crash
from TaxiMate import Routes
