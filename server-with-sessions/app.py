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

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return{}, 204
        
        user = User.query.filter_by(id=user_id)
        return UserSchema().dump(user), 200

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {'message': 'Logging out'}, 200

class Signup(Resource):
    def post(self):
        data = request.get_json()
        usernames = [user.username for user in User.query.all()]
        username = data.get('username')
        if username in usernames:
            raise ValueError("username must be unique")
        
        password = data.get('password')
        password_conformation = data.get('password_confirmation')
        if password != password_conformation:
            raise ValueError("passwords must match")
        
        user = User(username=username)
        user.password_hash = password

        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id

        return UserSchema().dump(user), 200

class NewPost(Resource):
    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()
        
        print(data)
        print(user_id)
        return {}

api.add_resource(HomePage, "/")
api.add_resource(Login, "/login")
api.add_resource(ViewUsers, "/users")
api.add_resource(ViewUser, "/users/<int:id>")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Logout, "/logout")
api.add_resource(Signup, "/signup")
api.add_resource(NewPost, "/newpost")

if __name__ == "__main__":
    app.run(port=5555, debug=True)