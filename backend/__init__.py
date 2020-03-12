import markdown
import os

# Import the framework
from flask import Flask
from flask_restful import Resource, Api, reqparse

# from .database import *

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

# Create the Parser
parser = reqparse.RequestParser()


@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class Homework1(Resource):

    def get(self, group_id):
        return

    def post(self, group_id):
        return


class Homework2(Resource):

    def delete(self, group_id, homework_id):
        return

    def put(self, group_id, homework_id):
        return


class Exams1(Resource):

    def get(self, group_id):
        return

    def post(self, group_id):
        return


class Exams2(Resource):

    def delete(self, group_id, exam_id):
        return

    def put(self, group_id, exam_id):
        return


class Groups1(Resource):

    def post(self):
        args = parser.parse_args()
        group_name = args['name']
        return group_name, 201


class Groups2(Resource):

    def get(self, group_id):
        return

    def delete(self, group_id):
        return

    def put(self, group_id):
        return group_id, 200


##
# Actually setup the Api resource routing here
##

api.add_resource(Homework1, '/groups/<group_id>/homework')
api.add_resource(Homework2, '/groups/<group_id>/homework/<homework_id>')
api.add_resource(Exams1, '/groups/<group_id>/exams')
api.add_resource(Exams2, '/groups/<group_id>/exams/<exam_id>')
api.add_resource(Groups1, '/groups')
api.add_resource(Groups2, '/groups/<group_id>')
