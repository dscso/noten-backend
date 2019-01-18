from flask import Flask
from flask_restful import Resource, Api
import db

app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        return {'version': '0.1'}



class Login(Resource):
    def post(self):
        return {
            "access_token":"MTQ0NjJkZmQ5OTM2NDE1ZTZjNGZmZjI3",
            "token_type":"bearer",
            "expires_in":3600,
            "refresh_token":"IwOGYzYTlmM2YxOTQ5MGE3YmNmMDFkNTVk",
            "scope":"create delete"
        }



api.add_resource(Home, '/')
api.add_resource(Login, '/login')
if __name__ == '__main__':
    app.run(debug=True)