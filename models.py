from database import db

class Post (db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    subject = db.Column("subject", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    rating = db.Column("rating", db.Integer)

    def __init__(self, subject, text, date):
        self.subject = subject
        self.text = text
        self.date = date

class User (db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(200))
    email = db.Column("email", db.String(50))
    password = db.Column("password", db.String(20))

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password


class Comment (db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column("text", db.String(100))

    def __init__(self, text):
        self.text = text
