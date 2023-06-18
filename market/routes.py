from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, jsonify, request
from market.models import User, Question, Topic
from market.forms import RegisterForm, LoginForm, CreateQuestion, CreateTopic
from validate_email import validate_email
from flask_login import login_user, logout_user
from market import db


@app.route('/')
def home_page():
    return render_template("home.html")


@app.route('/quiz')
def quiz_page():
    return render_template("quiz.html")


@app.route('/create/topic', methods=['GET', 'POST'])
def create_topic():
    form = CreateTopic()
    if request.method == 'POST':
        topic_data = request.form['topic']
        Topic.save_topic(topic_data)

    return render_template("/admin/add-topic.html", form=form)


@app.route('/create/question', methods=['GET', 'POST'])
def create_question():
    form = CreateQuestion()
    if request.method == 'POST':
        data = {
            'question': request.form['question'],
            'points': request.form['points'],
            'topic': request.form['topic'],
            'answer': request.form['answer'],

        }
        Question.save_question(data)

    form.populate_topic_choices()
    return render_template("/admin/add-question.html", form=form)


@app.route('/question', methods=['GET', 'POST'])
def question_page():
    questions = Question.query.filter_by().all()
    topics = Topic.query.all()
    if request.method == "POST" and request.form["topic_id"] != "all":
        questions = Question.query.filter_by(topic_id=request.form["topic_id"]).all()

    return render_template("questions.html", questions=questions, topics=topics)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        username_exists = user_to_create.username_exists(username=form.username.data)
        email_exist = user_to_create.email_exists(email=form.email.data)
        if username_exists:
            flash(f'Username already registered', category='danger')
        if email_exist:
            flash(f'Email already registered', category='danger')
        else:
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for("login_page"))
    if form.errors != {}:
        for err_mg in form.errors.values():
            flash(f'the is a problem with registration {err_mg}', category='danger')

    return render_template("register.html", form=form)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('quiz_page'))
        else:
            flash(f'Username and Password are not match', category='danger')

    return render_template("login.html", form=form)


@app.route('/check_correctness_of_value', methods=['POST'])
def check_username():
    checked_value = request.form["input-value"]
    input_name = request.form["inputName"]

    if input_name == "username":
        # Perform the database query to check if the username exists
        existing_value = User.query.filter_by(username=checked_value).first()
        min_length = RegisterForm.username.kwargs['validators'][0].min
        max_length = RegisterForm.username.kwargs['validators'][0].max

    if input_name == "email":
        # Perform the database query to check if the username exists
        existing_value = User.query.filter_by(email=checked_value).first()
        if not validate_email(checked_value):
            return jsonify({'available': False})

        min_length = RegisterForm.email.kwargs['validators'][0].min
        max_length = RegisterForm.email.kwargs['validators'][0].max

    if input_name == "password1":
        existing_value = ""
        min_length = RegisterForm.password1.kwargs['validators'][0].min
        max_length = RegisterForm.password1.kwargs['validators'][0].max

    if existing_value or (len(checked_value) < min_length and max_length > len(checked_value)):
        return jsonify({'available': False})
    else:
        return jsonify({'available': True})


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for("home_page"))
