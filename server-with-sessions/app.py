from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = "super-secret-key"

api = Api(app)

class HomePage(Resource):
    def get(self):
        return {"message": "Welcome to the page"}

api.add_resource(HomePage, "/")

if __name__ == "__main__":
    app.run(debug=True)