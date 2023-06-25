from sqlalchemy import func

import random

from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, logout_user, login_required
from sqlalchemy import func
from validate_email import validate_email

from market import app
from market import db
from market.forms import RegisterForm, LoginForm, CreateQuestion, CreateTopic
from market.helpers import *
from market.models import User, Question, Topic, Answer


@app.route('/')
def home_page():
    return render_template("home.html")


@app.route('/quiz', methods=['POST', 'GET'])
def quiz_page():
    if request.method == 'POST':
        # Clear necessary session before every usage
        clear_session(['topic_id', 'current_question', 'question_limit', 'user_score', 'all_questions'])

        # Generated list of random questions
        my_limit_questions = 3
        my_topic_id = request.form['topics']
        session['topic_id'] = my_topic_id
        session['current_question'] = 0
        session['question_limit'] = my_limit_questions

        random_questions = Question.query.filter(Question.topic_id == my_topic_id) \
            .order_by(func.random()) \
            .limit(my_limit_questions).all()

        session['user_score'] = session.get('user_score',
                                            [])  # Retrieve existing questions or initialize an empty list

        session['all_questions'] = session.get('all_questions',
                                               [])  # Retrieve existing questions or initialize an empty list
        for question in random_questions:
            print(f'{question.id} + {question.question}')
            question_data = {
                'id': question.id,
                'question': question.question,
                'topic_id': question.topic_id,
                'answer_id': question.answer_id,
                'points': question.points
                # Add other necessary attributes
            }
            session['all_questions'].append(question_data)
            print(session['all_questions'])

        # Redirect to questions
        return redirect(f'/quiz/question/{session["current_question"]}')

    else:
        # Get all possible topics for quiz
        topics = Topic.query.all()
        return render_template("/quiz/quiz.html", topics=topics)


# NEXT question
@app.route('/quiz/question/<int:question_order_id>')
def next_question(question_order_id):
    session['current_question'] = question_order_id
    actual_question = session['all_questions'][question_order_id]
    correct_answer = Answer.query.get(actual_question['answer_id'])
    session['correct_answer'] = correct_answer.id
    random_answers = Question.query.filter(Question.topic_id == session['topic_id'], Question.answer_id != correct_answer.id) \
        .order_by(func.random()) \
        .limit(3).all()

    answer_list = []
    for answer in random_answers:
        answer_list.append(answer.id)

    answers = Answer.query.filter(Answer.id.in_(answer_list)).all()
    answers.append(correct_answer)

    random.shuffle(answers)

    return render_template("/quiz/quiz-question.html", actual_question=actual_question, answers=answers)


@app.route("/check_answer_correctness", methods=['POST'])
def check_answer_correctness():
    user_answerID = int(request.form['answer_id'])
    correct_answerID = int(session['correct_answer'])
    session['user_score'] = session.get('user_score')  # Get session list

    question = Question.query.filter(Question.answer_id == correct_answerID).first()
    question_points = Question.get_points(correct_answerID)

    stats = {
        'question': question.id,
        'answered': True,
        'points': question_points,
    }

    correct_values_data = {
        'correct_answer_id': correct_answerID,
        'user_correct_answer': False,
        'finish_quiz': False
    }
    question_exists = any(stat['question'] == question.id for stat in session['user_score'])
    if correct_answerID == user_answerID:
        # Correct answer
        correct_values_data['user_correct_answer'] = True
        if not question_exists:
            session['user_score'].append(stats)
    else:
        # Incorrect answer
        if not question_exists:
            stats['points'] = 0
            session['user_score'].append(stats)

    if session['current_question']+1 == session['question_limit']:
        correct_values_data['finish_quiz'] = True
    return jsonify(correct_values_data)

@app.route('/quiz/finished')
def quiz_end():
    points = sum(stat['points'] for stat in session['user_score'])
    return render_template("/quiz/quiz_end.html", points=points)

@app.route('/create/topic', methods=['GET', 'POST'])
@login_required
def create_topic():
    form = CreateTopic()
    if request.method == 'POST':
        topic_data = request.form['topic']
        Topic.save_topic(topic_data)

    return render_template("/admin/add-topic.html", form=form)


@app.route('/create/question', methods=['GET', 'POST'])
@login_required
def create_question():
    form = CreateQuestion()
    if request.method == 'POST':
        data = {
            'question': request.form['question'],
            'points': request.form['points'],
            'topic': request.form['topic'],
            'answer': request.form['answer'],
            'quiz_answer': request.form['quiz_answer']

        }
        Question.save_question(data)

    form.populate_topic_choices()
    return render_template("/admin/add-question.html", form=form)


@app.route('/question', methods=['GET', 'POST'])
def question_page():
    # Get all topics from DB
    all_topics = Topic.query.all()
    data = []
    if request.method == "POST":
        # Get topics_list from multiple select
        topics_list = request.form.getlist('topics')
        data = Question.query.filter(Question.topic_id.in_(topics_list)).all()

    return render_template("questions.html", questions=data, topics=all_topics)


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
    session['logged_in'] = True
    session['quiz_started'] = False

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            # flash(f'You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('quiz_page'))
        else:
            flash(f'Username and Password are not match', category='primary')

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
@login_required
def logout_page():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for("home_page"))
