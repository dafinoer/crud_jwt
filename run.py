from flask import Flask
from flask_restful import Api
from apps.users.views import HelloWorld, Users, Items
from flask_jwt import JWT, jwt_required, current_identity
from utils.security import authenticate, identity


app = Flask(__name__)
api = Api(app=app)
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app=app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(HelloWorld, '/')
api.add_resource(Users, '/user/<string:name>')
api.add_resource(Items, '/users')

if __name__ == '__main__':
    app.run(debug=True)
