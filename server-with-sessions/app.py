from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = "super-secret-key"

api = Api(app)

class HomePage(Resource):
    def get(self):
        return {"message": "Welcome to the page"}

class Login(Resource):
    def post(self):
        
        username = request.get_json().get('username')
        password = request.get_json().get('password')

        return {"username": username, "password": password}, 200

api.add_resource(HomePage, "/")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(port=5555, debug=True)