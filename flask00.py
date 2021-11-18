# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Post as Post
from models import User as User
from forms import RegisterForm, LoginForm
import bcrypt
from flask import session


app = Flask(__name__)     # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mobilizePosts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
   db.create_all()   # run under the app context

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
   a_user =  db.session.query(User).filter_by(email='pyadav5@uncc.edu').one()
   return render_template('index.html', user = a_user)

@app.route('/feed')
def get_posts():
    if session.get('user'):
        my_posts = db.session.query(Post).all()

        return render_template('feed.html', posts=my_posts, user=session['user'])
    else:
        return redirect(url_for('signIn'))



@app.route('/feed/<post_id>')
#changed singlePost to feed
def get_post(post_id):
   a_user =  db.session.query(User).filter_by(email='pyadav5@uncc.edu').one()
   my_post = db.session.query(Post).filter_by(id=post_id).one()

   return render_template('singlePost.html', post=my_post, user=a_user)


@app.route('/feed/new',methods=['GET','POST'])
def new_post():
   # check method used for request
   if request.method == 'POST':
       # get title data
       subject = request.form["subject"]
       # get note data
       text = request.form['noteText']
       # create date stamp
       from datetime import date
       today = date.today()
       # format date mm/dd/yyyy
       today = today.strftime("%m-%d-%Y")
       new_record = Post(subject, text, today)
       db.session.add(new_record)
       db.session.commit()

       return redirect(url_for('get_posts'))
   else:
       # GET request -show new note form
       a_user =  db.session.query(User).filter_by(email='pyadav5@uncc.edu').one()
       return render_template('newPost.html', user=a_user)


# TO CHANGE
@app.route('/feed/edit/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
   #check method used for request
   if request.method == 'POST':
       # get title data
       subject = request.form['subject']
       # get note data
       text = request.form['noteText']
       post = db.session.query(Post).filter_by(id=post_id).one()
       # update note data
       post.subject = subject
       post.text = text
       # update note in DB
       db.session.add(post)
       db.session.commit()

       return  redirect(url_for('get_posts'))
   else:
       #GET request - show new note form to edit note
       # retrieve user from database
       a_user = db.session.query(User).filter_by(email='pyadav5@uncc.edu').one()

       # retrieve notes from database
       my_post = db.session.query(Post).filter_by(id=post_id).one()

       return render_template('newPost.html', post=my_post, user=a_user)


@app.route('/feed/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
   # retrieve note from database
   my_post = db.session.query(Post).filter_by(id=post_id).one()
   db.session.delete(my_post)
   db.session.commit()

   return redirect(url_for('get_posts'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_posts'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)




app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# post that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
