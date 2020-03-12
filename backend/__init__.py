import markdown
import os

# Import the framework
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from .database import *
from base64 import b64decode

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

# Create the Parser
parser = reqparse.RequestParser()


# Create Database-connection
database = Database()


def decode_password(password):
    password = b64decode((password[6:len(password)]))
    password = password.decode("utf-8")
    password = password[password.find(':')+1:len(password)]
    return password

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
        parser.add_argument('name')
        args = parser.parse_args()
        if args['name']:
            group_name = args['name']
            values = database.create_group(group_name)
            return values[2], values[1]
        else:
            return 400, 400


class Groups2(Resource):

    def get(self, group_id):
        try:
            group_id = int(group_id)
        except ValueError:
            return 400, 400
        values = database.get_group_name(group_id)
        if values[0]:
            return values[2], values[1]
        else:
            return values[1], values[1]

    def delete(self, group_id):
        parser.add_argument('Authorization', location='headers')
        args = parser.parse_args()
        password = decode_password(args['Authorization'])
        try:
            group_id = int(group_id)
        except ValueError:
            return 400, 400
        values = database.delete_group(group_id, password)
        return values[1], values[1]

    def put(self, group_id):
        parser.add_argument('name')
        parser.add_argument('Authorization', location='headers')
        args = parser.parse_args()
        password = decode_password(args['Authorization'])
        try:
            group_id = int(group_id)
        except ValueError:
            return 400, 400
        if args['name']:
            values = database.change_group_name(group_id, args['name'], password)
            return values[1], values[1]
        else:
            values = database.change_group_pass(group_id, password)
            if values[0]:
                return values[2], values[1]
            else:
                return values[1], values[1]


##
# Actually setup the Api resource routing here
##
api.add_resource(Homework1, '/groups/<group_id>/homework')
api.add_resource(Homework2, '/groups/<group_id>/homework/<homework_id>')
api.add_resource(Exams1, '/groups/<group_id>/exams')
api.add_resource(Exams2, '/groups/<group_id>/exams/<exam_id>')
api.add_resource(Groups1, '/groups')
api.add_resource(Groups2, '/groups/<group_id>')
