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


# @app.teardown_appcontext
# def teardown_db(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class homework(Resource):
    def get(self, todo_id):
        return {todo_id}


app.add_resource(homework, '/homework/<string:todo_id>')
