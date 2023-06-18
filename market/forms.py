from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_ckeditor import CKEditorField
from market.models import Topic


class RegisterForm(FlaskForm):
    username = StringField(label="Username: ", validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label="Email Address: ", validators=[Length(min=2, max=30), Email(), DataRequired()])
    password1 = PasswordField(label="Password: ", validators=[Length(min=2, max=50), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Register")


class LoginForm(FlaskForm):
    username = StringField(label="Username: ", validators=[DataRequired()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField(label="Login")


class CreateQuestion(FlaskForm):
    answer = CKEditorField('Answer:', validators=[DataRequired()])
    points = IntegerField(label='Points:', validators=[DataRequired()], render_kw={'type': 'number'})
    question = StringField(label='Question:', validators=[DataRequired()])
    topic = SelectField(label='Topic:', validators=[DataRequired()])

    def populate_topic_choices(self):
        self.topic.choices = [(topic.id, topic.topic) for topic in Topic.query.all()]


class CreateTopic(FlaskForm):
    topic = StringField(label='Topic:', validators=[DataRequired()])