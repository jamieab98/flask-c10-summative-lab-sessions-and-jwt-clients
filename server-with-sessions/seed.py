from app import app, db
from models import User, Note
from faker import Faker
import random

with app.app_context():

    print("Deleting old data")
    User.query.delete()
    Note.query.delete()

    fake = Faker()

    print("Creating users")
    users = []
    usernames = []

    i = 0
    while i < 10:
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.append(username)

        user = User(username=username)
        user.password_hash = "password123"

        users.append(user)

        i += 1
    
    db.session.add_all(users)
    db.session.commit()

    print("Creating notes")
    notes = []

    j = 0
    while j < 20:
        title = f'Title {j}'
        content = fake.paragraph()
        user_id = random.randint(1, 10)

        note = Note(title=title, content=content, user_id=user_id)
        notes.append(note)

        j += 1
    
    db.session.add_all(notes)
    db.session.commit()