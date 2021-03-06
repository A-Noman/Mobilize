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
from forms import RegisterForm
import bcrypt
from flask import session
from forms import LoginForm
from forms import CommentForm
from models import Comment as Comment
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])



app = Flask(__name__)     # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mobilizePosts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
   db.create_all()   # run under the app context

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return render_template('index.html', user=session['user'])
    return render_template("index.html")

@app.route('/feed')
def get_posts():
    if session.get('user'):
        my_posts = db.session.query(Post).filter_by(user_id=session['user_id']).all()


        return render_template('feed.html', posts=my_posts, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/allPosts')
def print_ALL():
    if session.get('user'):
        all_posts = db.session.query(Post).all()

        return render_template('allPosts.html', posts=all_posts, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/feed/<post_id>')
#changed singlePost to feed
def get_post(post_id):
    if session.get('user'):
        my_post = db.session.query(Post).filter_by(id=post_id, user_id=session['user_id']).one()

        form = CommentForm()

        return render_template('singlePost.html', post=my_post, user=session['user'], form=form)
    else:
        return redirect(url_for('login'))


@app.route('/allPosts/<post_id>')
def get_generalPost(post_id):
    if session.get('user'):
        the_post = db.session.query(Post).filter_by(id=post_id).one()

        form = CommentForm()

        return render_template('singlePost.html', post=the_post, user=session['user'], form=form)
    else:
        return redirect(url_for('login'))


@app.route('/feed/new',methods=['GET','POST'])
def new_post():
   if session.get('user'):
      # check method used for request
       if request.method == 'POST':
           # get title data
           subject = request.form["subject"]
           # get note data
           text = request.form['noteText']
           # get image file
           image_file = request.files['filename']
           # check if the image file has been uploaded
           if image_file.filename != '' and allowed_file(image_file.filename):
               ##image_file.save(image_file.filename)
               image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename))
               print('shreya : ' + image_file.filename)

           first_name = session['user']
           # create date stamp
           from datetime import date
           today = date.today()
           # format date mm/dd/yyyy
           today = today.strftime("%m-%d-%Y")

           rating = 0
           # new_record = Post(subject, text, today, session['user_id'], first_name)
           new_record = Post(subject, text, image_file.filename, today, rating, session['user_id'])
           db.session.add(new_record)
           db.session.commit()
           return redirect(url_for('get_posts'))
       else:
           # GET request -show new note form
           return render_template('newPost.html', user=session['user'])

   else:
       return redirect(url_for('login'))



# TO CHANGE
@app.route('/feed/edit/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if session.get('user'):

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

           # retrieve notes from database
           my_post = db.session.query(Post).filter_by(id=post_id).one()

           return render_template('newPost.html', post=my_post, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/feed/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    if session.get('user'):
       # retrieve note from database
       my_post = db.session.query(Post).filter_by(id=post_id).one()
       db.session.delete(my_post)
       db.session.commit()

       return redirect(url_for('get_posts'))
    else:
        return redirect(url_for('login'))



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

        quote = "this is a quote"
        color = "COLOR"
        hobbies = "a hobby"
        courses = "software tings"

        # new constructor

        new_user = User(first_name, last_name, request.form['email'], h_password, quote, color, hobbies, courses)

        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('print_ALL'))

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
        if (request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('print_ALL'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))


@app.route('/feed/<post_id>/comment', methods=['POST'])
def new_comment(post_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(post_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_generalPost', post_id=post_id))

    else:
        return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if session.get('user'):
        user = db.session.query(User).filter_by(id=session['user_id']).one()

        return render_template('profile.html', User=user, user=session['user'])

    else:
        return redirect(url_for('login'))


@app.route('/profile/update', methods=['POST'])
def update_profile():
    if session.get('user'):

        newQuote = request.form['quote']
        newColor = request.form['color']
        newHobbies = request.form['hobbies']
        newCourses = request.form['courses']

        user = db.session.query(User).filter_by(id=session['user_id']).one()

        user.quote = newQuote
        user.color = newColor
        user.hobbies = newHobbies
        user.courses = newCourses

        db.session.add(user)
        db.session.commit()

        user = db.session.query(User).filter_by(id=session['user_id']).one()

        return redirect(url_for('profile'))

    else:
        return redirect(url_for('login'))


# stone

@app.route('/credentials')
def credentials():
   if session.get('user'):
       the_user = db.session.query(User).filter_by(id=session['user_id']).one()

       return render_template('credentials.html', user = the_user)


@app.route('/credentials/update', methods=['POST'])
def updatePersonalInformation():

  if session.get('user'):

      email = request.form['email']
      currentPassword = request.form['currentPassword']
      newPassword = request.form['newPassword']
      user = db.session.query(User).filter_by(id = session['user_id']).one()

      # update user data

      if currentPassword == user.password:
          user.email = email
          user.password = newPassword
          db.session.add(user)
          db.session.commit()


      # update username and password in DB


  return render_template('credentials.html', User=user, user=session['user'])


@app.route('/singlePost/<post_id>/rate', methods=['POST'])
def upvote(post_id):
    if session.get('user'):
       # retrieve note from database
       my_post = db.session.query(Post).filter_by(id=post_id).one()

       my_post.rating = my_post.rating+1
       db.session.add(my_post)
       db.session.commit()

       form = CommentForm()

       return render_template('singlePost.html', post=my_post, user=session['user'], form=form)

    else:
        return redirect(url_for('login'))

@app.route('/singlePost/<post_id>/undo', methods=['POST'])
def undo(post_id):
    if session.get('user'):
       # retrieve note from database
       my_post = db.session.query(Post).filter_by(id=post_id).one()

       my_post.rating = my_post.rating - 1
       db.session.add(my_post)
       db.session.commit()

       form = CommentForm()

       return render_template('singlePost.html', post=my_post, user=session['user'], form=form)

    else:
        return redirect(url_for('login'))


@app.route('/display/<filename>')
def display_image(filename):
  #print('display_image filename: ' + filename)
  return redirect(url_for('static', filename=filename), code=301)


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# post that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
