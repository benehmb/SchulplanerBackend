import markdown
import os
import shelve

# Import the framework
from flask import Flask, request
from flask_restful import Resource, Api
from .database import *

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

database = Database()


@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)