import markdown
import os

# Import the framework
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from .database import *
from base64 import b64decode

# Create an instance of Flask
app = Flask(__name__)
CORS(app)

# Create the API
api = Api(app)

# Create the Parser
parser = reqparse.RequestParser()

# Create Database-connection
database = Database()


def decode_password(password):
    password = b64decode((password[6:len(password)]))
    password = password.decode("utf-8")
    password = password[password.find(':') + 1:len(password)]
    return password


@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


# noinspection PyMethodMayBeStatic
class Homework1(Resource):

    def get(self, group_id):
        try:
            group_id = int(group_id)
        except ValueError:
            return 400, 400
        values = database.get_homework(group_id)
        if values[0]:
            return values[2], values[1]
        else:
            return values[1], values[1]

    def post(self, group_id):
        try:
            group_id = int(group_id)
        except ValueError:
            return 400, 400
        parser.add_argument('Authorization', location='headers')
        parser.add_argument('date')
        parser.add_argument('subject')
        parser.add_argument('homework')
        args = parser.parse_args()
        password = decode_password(args['Authorization'])
        if args['date'] and args['subject'] and args['homework']:
            values = database.add_homework(group_id=group_id, date=args['date'], subject=args['subject'],
                                           homework=args['homework'], password=password)
            return values[1], values[1]
        else:
            return 400, 400


# noinspection PyMethodMayBeStatic
class Homework2(Resource):

    def delete(self, group_id, homework_id):
        try:
            group_id = int(group_id)
            homework_id = int(homework_id)
        except ValueError:
            return 400, 400
        parser.add_argument('Authorization', location='headers')
        args = parser.parse_args()
        password = decode_password(args['Authorization'])
        values = database.delete_homework(homework_id=homework_id, group_id=group_id, password=password)
        return values[1], values[1]

    def put(self, group_id, homework_id):
        try:
            group_id = int(group_id)
            homework_id = int(homework_id)
        except ValueError:
            return 400, 400
        parser.add_argument('Authorization', location='headers')
        parser.add_argument('date')
        parser.add_argument('subject')
        parser.add_argument('homework')
        args = parser.parse_args()
        password = decode_password(args['Authorization'])
        if args['date'] and args['subject'] and args['homework']:
            values = database.edit_homework(homework_id=homework_id, group_id=group_id, date=args['date'],
                                            subject=args['subject'], homework=args['homework'], password=password)
            return values[1], values[1]
        else:
            return 400, 400


# noinspection PyMethodMayBeStatic
class Exams1(Resource):

    def get(self, group_id):
        try:
            group_id = int(group_id)
        except ValueError:
            return 400, 400
        values = database.get_exams(group_id)
        if values[0]:
            return values[2], values[1]
        else:
            return values[1], values[1]

    def post(self, group_id):
        try:
            group_id = int(group_id)
        except ValueError:
            return 400, 400
        parser.add_argument('Authorization', location='headers')
        parser.add_argument('date')
        parser.add_argument('subject')
        parser.add_argument('exam')
        args = parser.parse_args()
        password = decode_password(args['Authorization'])
        if args['date'] and args['subject'] and args['exam']:
            values = database.add_exam(group_id=group_id, date=args['date'], subject=args['subject'], exam=args['exam'],
                                       password=password)
            return values[1], values[1]
        else:
            return 400, 400


# noinspection PyMethodMayBeStatic
class Exams2(Resource):

    def delete(self, group_id, exam_id):
        try:
            group_id = int(group_id)
            exam_id = int(exam_id)
        except ValueError:
            return 400, 400
        parser.add_argument('Authorization', location='headers')
        args = parser.parse_args()
        password = decode_password(args['Authorization'])
        values = database.delete_exam(exam_id=exam_id, group_id=group_id, password=password)
        return values[1], values[1]

    def put(self, group_id, exam_id):
        try:
            group_id = int(group_id)
            exam_id = int(exam_id)
        except ValueError:
            return 400, 400
        parser.add_argument('Authorization', location='headers')
        parser.add_argument('date')
        parser.add_argument('subject')
        parser.add_argument('exam')
        args = parser.parse_args()
        password = decode_password(args['Authorization'])
        if args['date'] and args['subject'] and args['exam']:
            values = database.edit_exam(exam_id=exam_id, group_id=group_id, date=args['date'], subject=args['subject'],
                                        exam=args['exam'], password=password)
            return values[1], values[1]
        else:
            return 400, 400


# noinspection PyMethodMayBeStatic
class Groups1(Resource):

    def post(self):
        parser.add_argument('name')
        args = parser.parse_args()
        if args['name']:
            group_name = args['name']
            values = database.create_group(name=group_name)
            return values[2], values[1]
        else:
            return 400, 400


# noinspection PyMethodMayBeStatic
class Groups2(Resource):

    def get(self, group_id):
        try:
            group_id = int(group_id)
        except ValueError:
            return 400, 400
        values = database.get_group_name(group_id=group_id)
        parser.add_argument('Authorization', location='headers')

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
        if args['Authorization']:
            values = database.check_group_pass(group_id=group_id, password=decode_password(args['Authorization']))
            return values[1], values[1]
        else:
            values = database.delete_group(group_id=group_id, password=password)
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
            values = database.change_group_name(group_id=group_id, name=args['name'], password=password)
            return values[1], values[1]
        else:
            values = database.change_group_pass(group_id=group_id, old_password=password)
            if values[0]:
                return values[2], values[1]
            else:
                return values[1], values[1]


##
# Actually setup the Api resource routing here
##
api.add_resource(Homework1, '/groups/<group_id>/homework', '/groups/<group_id>/homework/')
api.add_resource(Homework2, '/groups/<group_id>/homework/<homework_id>', '/groups/<group_id>/homework/<homework_id>/')
api.add_resource(Exams1, '/groups/<group_id>/exams', '/groups/<group_id>/exams/')
api.add_resource(Exams2, '/groups/<group_id>/exams/<exam_id>', '/groups/<group_id>/exams/<exam_id>/')
api.add_resource(Groups1, '/groups', '/groups/')
api.add_resource(Groups2, '/groups/<group_id>', '/groups/<group_id>/')
