from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
# gain access to the users resource
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
# call UserRegister + functions
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
