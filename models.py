from database import db
import datetime

class Post(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    subject = db.Column("subject", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    rating = db.Column("rating", db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, subject, text, date, rating, user_id):
        self.subject = subject
        self.text = text
        self.date = date
        self.rating = rating
        self.user_id = user_id

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    posts = db.relationship("Post", backref="user", lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()


class Comment(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column("text", db.String(100))

    def __init__(self, text):
        self.text = text
