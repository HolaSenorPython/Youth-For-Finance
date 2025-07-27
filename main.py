# Import statements
from datetime import date # Date for community service logging
from flask import Flask, redirect, url_for, flash, render_template, request, abort, session
from flask_bootstrap import Bootstrap5
from forms import ContactForm, RegisterUserForm, LoginForm, AddTaskForm, DeleteTaskForm, NukeForm # Import all our forms necessary
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required # Imports for USER handling stuff
from functools import wraps # for officer only stuff later
# Whole lotta database stuff.
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Date
# User password handling
from werkzeug.security import generate_password_hash, check_password_hash # will hash their passwords, just makes things more secure
import os
import smtplib # For contacting and stuff
from email.message import EmailMessage # also for sending emails, but we making it a lil more steps so we can send emojis
from dotenv import load_dotenv
# Image handling
from werkzeug.utils import secure_filename

load_dotenv() # LOAD ALL ENV VARIABLES

# Define email sending function
def send_email(name, email, message):
    my_email = os.environ.get('MY_EMAIL_FOR_USER')
    my_pass = os.environ.get('MY_PASS_FOR_USER')
    # Variables for later
    users_name = name
    users_email = email
    users_msg = message
    # Officer's emails:
    ajay_email = os.environ.get('AJAY_EMAIL')
    gio_email = os.environ.get('GIO_EMAIL')
    chris_b_email = os.environ.get('CHRIS_B_EMAIL')
    gabby_email = os.environ.get('GABBY_EMAIL')
    my_personal_email = os.environ.get('MY_PERSONAL_EMAIL')

    # Make email msg object
    msg = EmailMessage()
    msg['Subject'] = f"You've received a contact form message from: {users_name}!"
    msg['From'] = my_email # Has to be MY email so google doesn't trip and assume im a bot
    msg['To'] = [my_personal_email, gio_email, ajay_email, chris_b_email, gabby_email]
    msg['Reply-To'] = users_email # ANY officer reply goes to their (the contact form filler outer) email

    # Actually make message body / content
    body = f"""\
Name: {users_name}
Email: {users_email}
Location: Youth For Finance Website

Message: {users_msg}
"""
    msg.set_content(body, charset='utf-8') # Set this body multiline string as the email content, and make sure the charset is utf 8 for emojis and stuff

    # NOW actually send mail
    try: # Error handling 😏
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_pass) # type: ignore # Login to my acc😉
            connection.send_message(msg=msg) # Send our email, with the message being out email message object
        return True # return true if everything went well
    except Exception as e:
        print(f"Error sending email: {e}")
        return False # otherwise return false


app = Flask(__name__) # App is located at the name of whatever this file is called (main)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY") # Set flask key
app.config['UPLOAD_FOLDER'] = 'static/assets/img/uploads' # THIS IS WHERE ALL USER UPLOADS FOR COMMUNITY SERVICE GO
Bootstrap5(app=app) # Setup bootstrap5

# Configure Flask login manager (THIS LETS ME DISALLOW PEOPLE FROM ACCESSING PAGES WHEN NOT LOGGED IN!)
login_manager = LoginManager()
login_manager.login_view = 'login' # type: ignore # Name of my login route function
login_manager.login_message = "You must be logged in to access this page."
login_manager.init_app(app=app) 

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
# Had to use absolute path cause it was tripping
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app=app)

# CREATE OUR TABLES!
class User(db.Model, UserMixin): # Inherit from UserMixin in Flask, lets me check if a user is loggin in and take action from there
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Every user has an ID, this is the PRIMARY key because it will NOT require me putting it in and flask will track it
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False) # Every email is unique, and every user MUST have an email, no MORE than 100 chars
    password: Mapped[str] = mapped_column(String(100), nullable=False) # no MORE than 100 chars, not nullable
    name: Mapped[str] = mapped_column(String(50), nullable=False) # no MORE than 50 chars, non nullable

    # THIS IS THE LINK TO THE TASKS TABLE!!! EVERY USER HAS TASKS ASSOCIATED WITH THEM.
    tasks = relationship("Task", back_populates="taskdoer") # This is also a list that can be iterated through.

class Task(db.Model):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # and that taskdoer has an id, which should equal the id of a user in the user table (this is a link)
    taskdoer_id: Mapped[int] = mapped_column(Integer, ForeignKey("Users.id")) # not USER as in the class name but "USERS" as in the table name
    # Every task has ONE task doer (every task relates back to a user)
    taskdoer = relationship("User", back_populates="tasks")
    # and it should also have something to measure the amount of time it took, and what it was
    task_description: Mapped[str] = mapped_column(String(300), nullable=False)
    time_taken: Mapped[int] = mapped_column(Integer, nullable=False)
    # NEW FEATURE RECOMMENDED BY ARIEL: Date verifcation and proof image of activity
    date_completed: Mapped[date] = mapped_column(Date, nullable=False)
    proof_image: Mapped[str] = mapped_column(String(200), nullable=False) # STIRNG FILE NAME of the Image

# THIS CODE IS SO THAT THE USER GETS RETAINED USING FLASK_LOGIN ACROSS DIFFERENT PAGES
@login_manager.user_loader
def load_user(user_id): # Will take a user id as an input
    return db.session.get(User, user_id)

# Defined admin ids globally to work with it in other functions
admin_ids = [1, 2, 3, 4, 5, 6, 7] # IDS of the admin users (first 7 people)

# THIS IS MY CUSTOM ADMIN DECORATOR. OFFICERS WILL GET ACCESS TO A SECRET PAGE!
def admin_only(function):
    @wraps(function) # Preserves the name of the actual function passed in. This is built in flask stuff so nothing breaks?
    def admin_check(*args, **kwargs):
        if current_user == None:
            return redirect(url_for('login'))
        elif current_user.id in admin_ids:
            return function(*args, **kwargs) # Return the function in question if they are an admin user (have one of ids)
        else:
            return abort(403)
    return admin_check # return the admin check function's result, not the function passed in by itself or anything else

@app.route('/')
def home(): # The home page will vary based on who's logged in so yeah pass those bad boys in.
    return render_template("index.html", logged_in=current_user.is_authenticated, user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit(): # IF A POST REQUEST IS MADE
        user_email = form.email.data
        user_password = form.password.data
        user_name = form.name.data
        session['user_pass_unhashed'] = user_password # SAVE UNHASHED PASS IN SESSION, SO WE CAN ACCESS IT IN THE USER HOME PG FUNCTION LATER
        # First, lets search if a user with this email is already in the system
        result = db.session.execute(db.select(User).where(User.email == user_email))
        user = result.scalar() # And pull one object (user) from our search

        if user: # If there IS a user already in the db with that email...
            flash(f"There is already a registered account with the email {user_email}!", category='info')
            return(redirect(url_for('login'))) # Take them to login page
        
        # This gets executed if there ISN'T a user with that email, therefore we can create 😏
        salty_password = generate_password_hash(user_password, 'pbkdf2:sha256', salt_length=8) # type: ignore # random salt should have length of 8
        # Make new user
        new_user = User(
            email=user_email, # type: ignore
            password=salty_password, # type: ignore
            name=user_name # type: ignore
        )
        db.session.add(new_user) # Add our new user to the db
        db.session.commit() # Commit these changes/update db

        login_user(new_user) # Login this user with flask
        flash(f"Successfully registered as {user_name}.", category='success')
        return(redirect(url_for('user_home'))) # Take them to their home page
    
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # IF A POST REQUEST IS MADE (if it was submitted and validated)
        email = form.email.data
        password = form.password.data
        session['user_pass_unhashed'] = password # SAVE UNHASHED PASS IN SESSION, SO WE CAN ACCESS IT IN THE USER HOME PG FUNCTION LATER
        # First make sure there is an account to login to, and also that there arent multiple accounts with the same email(try except is PERFECT for this)
        try:
            requested_user = db.session.execute(db.select(User).where(User.email == email)).scalar_one() # type: ignore
        except NoResultFound:
            flash("The requested user doesn't exist in our database! Maybe try registering instead?", category='warning')
            return redirect(url_for('register'))
        except MultipleResultsFound:
            flash("Something is wrong. Multiple accounts have the same email. Contact Elisha for help.", category='danger')
            return(redirect(url_for('contact')))

        # This gets executed if none of the exceptions above affected our "requested user"
        password_check = check_password_hash(requested_user.password, password) # type: ignore

        # If it passes password check
        if password_check:
            login_user(requested_user) # Log them in!
            flash(f"Successfully logged in as {requested_user.name}.", 'success')
            return(redirect(url_for('user_home'))) # type: ignore
        else:
            flash("Error: incorrect password.", 'danger')
            return redirect(url_for('login'))
    
    return render_template("login.html", form=form)

# Logout route n function
@app.route('/logout')
@login_required # Need to be logged in to log out. duhhh. 
def logout():
    logout_user() # Log them out
    return redirect(url_for('home')) # Send them back to the main page/home page

@app.route('/contact-us', methods=['GET', 'POST'])
def contact():
    email_sent = None # Starts out as none, to prevent any errors later, it must exist
    contact_form = ContactForm()
    if contact_form.validate_on_submit(): # if post request is made...
        user_name = contact_form.name.data
        user_email = contact_form.email.data
        user_message = contact_form.message.data
        email_sent = send_email(user_name, user_email, user_message) # Function will return smth
        if email_sent:
            flash("Email sent successfully!🎉 One of us should get back to you shortly.", category='success')
        else:
            flash("Oops! There was an error in sending your email. Try again or contact Elisha in person.", category='danger')
        return redirect(url_for('contact', email_sent=email_sent)) # Redirect back to contact page and show message
    
    # Now since we are REDIRECTING, and the form will be refreshed, we must capture the result of that email sent function,
    # using the below code, and that result is also found in our URL as a parameter.
    email_sent_param = request.args.get('email_sent')
    if email_sent_param == 'True': # This is not a normal boolean - its the parameter up there in our link
        email_sent = True
    elif email_sent_param == 'False':
        email_sent = False

    return render_template('contact.html', form=contact_form, email_sent=email_sent) # take contact form as form parameter and email sent as email sent lol

# THIS IS THE ACTUAL PAGE WHERE LOGGED IN USERS WILL SEE THEIR HOURS, AND LOG HOURS
@app.route('/user-home')
@login_required # Login required decorator from flask :D
def user_home():
    is_admin = None
    # Do a quick admin check, this will let me dynamically update HTML based on if they are admin
    if current_user.id in admin_ids:
        is_admin = True
    else:
        is_admin = False
    # Get all the tasks that have the same id as our current user
    tasks = current_user.tasks
    # Get the user's unhashed pass so we can work with it using our js (show n hide)
    unhashed_pass = session.get('user_pass_unhashed')
    # Sum all the user's hours beforehand, and pass it into the html doc for jinja
    total_serv_hrs = sum(task.time_taken for task in current_user.tasks)
    # Get the titles of all the columns in the task database so we can utilize it in the html table using jinja
    column_titles = Task.__table__.columns.keys() # type: ignore
    clean_titles = [title.replace("_", " ").title() for title in column_titles] # Clean em up so they look pretty

    return render_template('user-home.html', user=current_user, total_hours=total_serv_hrs, 
                           unhashed_password=unhashed_pass, titles=clean_titles, tasks=tasks, is_admin=is_admin)

@app.route('/add-service', methods=['GET', 'POST'])
@login_required # Login required decorator from flask :D
def add_service():
    form = AddTaskForm()
    if form.validate_on_submit(): # IF A POST REQUEST IS MADE
        task_desc = form.service_description.data
        time_taken = form.time_taken.data
        le_date = form.date.data
        # Handle image stuff
        image_file = form.proof_image.data
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path) # Save the image at the path above (our uploads folder for users)
        # Init task obj (WE DONT NEED TO SPECIFY TASKDOER ID: OUR FOREIGN KEY HANDLES THIS.)
        new_task = Task(
            taskdoer=current_user, # type: ignore
            task_description=task_desc, # type: ignore
            time_taken=time_taken, # type: ignore
            date_completed=le_date,  # type: ignore
            proof_image=filename,  # type: ignore # SAVE SHORTEnED FILE NAME in DB, this is WAYYYY better than storing the real file in there lol for this tiny app
            )
        db.session.add(new_task) # Add our task to the db
        db.session.commit() # Commit these changes
        return(redirect(url_for('user_home', user=current_user))) # Redirect to user home with our current user as the user param
    
    return render_template('add-task.html', form=form, user=current_user)

# Route for deleting a task
@app.route('/delete-service', methods=['GET', 'POST'])
@login_required # Login required decorator from flask :D
def del_service():
    form = DeleteTaskForm()
    if form.validate_on_submit(): # IF A POST REQUEST IS MADE...
        requested_task_id = form.desired_task_id.data
        targeted_task = db.get_or_404(Task, requested_task_id) # Get the task with the requested ID, or force an error
        targeted_task_desc = targeted_task.task_description # Grab desc for msg flashing

        # If they ATTEMPT to DELETE A TASK THAT ISNT THEIRS, AND THEY ARENT ADMIN, SEND EM BACK!
        if targeted_task.taskdoer_id != current_user.id and current_user.id not in admin_ids:
            flash("You can't delete that task, it isn't yours!", 'danger')
            return redirect(url_for('user_home', user=current_user))
        # Else if the current user is not the taskdoer, but an admin...
        elif targeted_task.taskdoer_id != current_user.id and current_user.id in admin_ids:
            flash(f"Successfully deleted '{targeted_task.taskdoer.name}'s' task with the following description: {targeted_task_desc}", "success")
            return redirect(url_for('user_home', user=current_user))
        # Delete it if the above doesn't apply to them!
        db.session.delete(targeted_task)
        db.session.commit() # Commit changes
        # Flash and redirect
        flash(f"Successfully deleted your task.", 'success')
        return redirect(url_for('user_home', user=current_user, logged_in=current_user.is_authenticated))
    
    return render_template('delete-task.html', form=form, user=current_user)

# Final route. Route for ADMIN users (officers)
@app.route('/admin-page')
# DECORATORS ARE BOTTOM UP, BUT IN ADMIN ONLY, DEPENDING ON WHAT HAPPENS WE MAKE A HIT TO THIS ROUTE, MEANING WE WILL NEED TO CHECK IF THEY ARE LOGGED IN AFTER THE HIT
@login_required # Login needed duh
@admin_only # Only admins can access
def admin_page():
    all_users = User.query.all() # Get EVERY USER in db
    all_tasks = Task.query.all() # Get EVERY TASK in db
    return render_template('admin.html', user=current_user, all_users=all_users, all_tasks=all_tasks)

# SECRET NUKE ROUTE
@app.route('/nuke', methods=['GET', 'POST'])
@login_required # must be logged in
@admin_only # only admins
def nuke():
    form = NukeForm()
    if form.validate_on_submit():
        nuke_answer = form.nuke_db.data
        if nuke_answer: # If they checked the box
            Task.query.delete()
            User.query.delete()
            db.session.commit()
            flash("Database wiped!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Database was retained, you didn't check the box.", 'warning')
            return redirect(url_for('user_home'))
        
    return render_template('nuke.html', form=form)
# Instructions to run app (only here)
if __name__ == "__main__":
    app.run(debug=False) # Debug mode on