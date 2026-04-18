from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_migrate import Migrate
from models import db, Note, NoteSchema, User, UserSchema

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class HomePage(Resource):
    def get(self):
        return {"message": "Welcome to the page"}

class Login(Resource):
    def post(self):
        
        username = request.get_json().get('username')
        password = request.get_json().get('password')

        return {"username": username, "password": password}, 200

class ViewUsers(Resource):
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True)
        return schema.dump(users), 200
    
api.add_resource(HomePage, "/")
api.add_resource(Login, "/login")
api.add_resource(ViewUsers, "/users")

if __name__ == "__main__":
    app.run(port=5555, debug=True)