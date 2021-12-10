from database import db
import datetime

class Post(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    subject = db.Column("subject", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    rating = db.Column("rating", db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan", lazy=True)

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
    comments = db.relationship("Comment", backref="user", lazy=True)
    # Profile stuff
    quote = db.Column("quote", db.String(100), nullable=True, default="test")
    color = db.Column("color", db.String(100), nullable=True, default="ooo")
    hobbies = db.Column("hobbies", db.String(100), nullable=True, default="ooo")
    courses = db.Column("courses", db.String(100), nullable=True, default="ooo")

    def __init__(self, first_name, last_name, email, password, quote, color, hobbies, courses):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()

        self.quote = quote
        self.color = color
        self.hobbies = hobbies
        self.courses = courses


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, content, post_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.post_id = post_id
        self.user_id = user_id
