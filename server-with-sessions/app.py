from flask import Flask, jsonify, request, session
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
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValueError("User does not exist")
        
        password = request.get_json().get('password')
        if not user.authenticate(password):
            raise ValueError("incorrect password")
        
        session['user_id'] = user.id
        return {'message': 'successful login'}, 200

class ViewUsers(Resource):
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True)
        return schema.dump(users), 200

class ViewUser(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return UserSchema().dump(user), 200

class ViewNotes(Resource):
    def get(self):
        notes = Note.query.all()
        schema = NoteSchema(many=True)
        return schema.dump(notes), 200

class CheckSession(Resource):
    def get(self):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        return UserSchema().dump(user), 200

api.add_resource(HomePage, "/")
api.add_resource(Login, "/login")
api.add_resource(ViewUsers, "/users")
api.add_resource(ViewUser, "/users/<int:id>")
api.add_resource(ViewNotes, "/notes")
api.add_resource(CheckSession, "/check_session")

if __name__ == "__main__":
    app.run(port=5555, debug=True)