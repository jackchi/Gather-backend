# allows py to interact w/ sqlite3
import sqlite3
from flask_restful import Resource, reqparse
#from flask_jwt import jwt_required


class User:
    TABLE_NAME = 'users'

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # initialize connection
        connection = sqlite3.connect('data.db')
        # initialize cursor
        cursor = connection.cursor()

        # search through table for given username
        query = "SELECT * FROM {table} WHERE username=?".format(
            table=cls.TABLE_NAME)
        # params must always be in form of a tupple--> use ending comma
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            # return user object w/ data from that row
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    # create required name/pw fields
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be blank.")

    def post(self):
        # use the parser / get data from JSON payload
        data = UserRegister.parser.parse_args()

        # find by username
        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        # connection to database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # insert values into table. 1st id must be NULL in order to auto-increment. "?"s == username argument, pw argument.
        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(
            table=self.TABLE_NAME)
        # username/pw must be in tuple
        cursor.execute(query, (data['username'], data['password']))

        # save to disk
        connection.commit()
        # close connection
        connection.close()

        return {"message": "User created successfully."}, 201
