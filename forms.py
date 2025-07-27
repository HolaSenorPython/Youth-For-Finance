from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, IntegerField, DateField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed

# Form for Contacting Us
class ContactForm(FlaskForm):
    email = EmailField(label="What is your email? (Personal, NOT school)", validators=[DataRequired(), Email()]) # I WILL for contact form though.
    name = StringField(label="What is your name?", validators=[DataRequired()])
    message = StringField(label="Write your message below.", validators=[DataRequired()])
    submit = SubmitField(label="Submit Form📝")

# Form for Registering as a New user
class RegisterUserForm(FlaskForm):
    email = StringField(label="Email:", validators=[DataRequired()]) # String field, I WONT DO EMAIL VERIFICATION.
    password = PasswordField(label="Password:", validators=[DataRequired()])
    name = StringField(label="First and Last Name:", validators=[DataRequired()])
    sign_up_btn = SubmitField("Sign me up!💵")

# Form for Login!
class LoginForm(FlaskForm):
    email = StringField(label="Email:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    login_btn = SubmitField("Let me in!🗿")

# Form for Adding a Community Service Act / Task
class AddTaskForm(FlaskForm):
    service_description = StringField("Describe your community service act in 300 characters or less.", validators=[DataRequired()])
    time_taken = IntegerField("How many hours was this?⌚", validators=[DataRequired()])
    date = DateField("When was this activity completed?", validators=[DataRequired()])
    proof_image = FileField("Upload Image Proof:", validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])]) # These are the file types we want
    submit_hrs = SubmitField("Log Hours & Activity!🤩")

# Form for DELETING a Task / Community Service Act
class DeleteTaskForm(FlaskForm):
    desired_task_id = IntegerField("What is the ID of the task you would like to remove?", validators=[DataRequired()])
    delete_task_btn = SubmitField("Delete Task!🗑️", render_kw={'class': 'btn btn-danger'}) # Specify keywords for render, specifically render button with those classes on it

# Admin form for NUKING the database
class NukeForm(FlaskForm):
    nuke_db = BooleanField("Check the box if you are SURE you want to reset all databases.")
    submit_answer = SubmitField("I have my answer.🫵")