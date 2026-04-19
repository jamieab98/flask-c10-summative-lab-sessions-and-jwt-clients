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
        if not user_id:
            return {'message': 'must be logged in to create a new message'}
        data = request.get_json()
        
        newNote = Note(title=data['title'], content=data['content'], user_id=user_id)
        
        db.session.add(newNote)
        db.session.commit()

        return NoteSchema().dump(newNote), 201

class UpdatePost(Resource):
    def patch(self, id):
        updatedcontent = request.get_json().get('updatedContent')
        user_id = session.get('user_id')
        usersNotesIDs = [note.id for note in Note.query.filter_by(user_id=user_id)]

        if id not in usersNotesIDs:
            return {'message': 'user can only modify their own note'}, 403
        
        note = Note.query.filter_by(id=id).first()
        note.content = updatedcontent

        db.session.commit()

        return NoteSchema().dump(note), 202

class ViewUsersPosts(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'message': 'must be logged in to view notes'}
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        
        usersNotes = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)

        return NoteSchema(many=True).dump(usersNotes.items), 200

class DeleteNote(Resource):
    def delete (self, id):
        user_id = session.get('user_id')
        if not user_id:
            return{"message": "must be logged in to delete a note"}
        
        note = Note.query.filter_by(id=id).first()
        if not note:
            return{"message": "the requested not does not exit"}
        
        if not note in Note.query.filter_by(user_id=user_id):
            return{"message": "cannot delete another user's note"}
        
        
        return{}
    

api.add_resource(HomePage, "/")
api.add_resource(Login, "/login")
api.add_resource(ViewUsers, "/users")
api.add_resource(ViewUser, "/users/<int:id>")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Logout, "/logout")
api.add_resource(Signup, "/signup")
api.add_resource(NewPost, "/newpost")
api.add_resource(UpdatePost, "/updatenotecontent/<int:id>")
api.add_resource(ViewUsersPosts, "/userpost")
api.add_resource(DeleteNote, "/deletepost/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)