Title: flask-c10-summative-lab-sessions-and-jwt-clients

Description: This application that stores notes. In order for a user to access stored notes, they have to log in. If they successfully log in, they 
can access notes made by themselves. There are endpoint that would allow the user to create a new note, modify a note, or delete a note. New users 
are also able to create an account so they can begin to create, view, modify, and delete their own notes.

Installation: To get the application working, download the folder from github and open the project. In the console, run "pipenv install" and the "pipenv shell"
to create and activate the virtual environment. Run the following commands to install the necessary dependencies:
    pip install flask
    pip install flask_restful
    pip install flask_migrate
    pip install faker
    pip install random
    pip install flask_sqlalchemy
    pip install marshmallow
    pip install werkzeug

Seeding the database: Within the server directory, run the following commands to seed the database:
    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade head
    python3 seed.py

Starting the application: Within the server directory, run the follwing command to start the application:
    python3 app.py

Endpoints
    "/" - Bring the user to the home page which just welcomes them the page.

    "/login" - Takes a username and password from the user and checks to see if it is a stored username password combination. If it is, the user is logged in and the session['user_id'] is saved.

    "/users" - Shows all users for testing purposes

    "/users/<int:id>" - Shows a specific user for testing purposes

    "/check_session" - Checks to see if a user is logged in by sessing if session.get('user_id') returns anything.

    "/logout" - Logs the user out of the application by setting session['user_id'] to None.

    "/signup" - Allows a new user to create login credentials and save them for future use.

    "/newpost" - Allows a logged in user to create a new note that will only be accessible to that user.

    "/updatepost/<int:id>" - Allows a note to be modified by the user that created the note.

    "/userpost" - Shows a user all of their notes.

    "/deletepost<int:id>" - Allows a user to delete posts that the specified user created in the past.