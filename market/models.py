from market import db
from market import bcrypt
from market import login_manager
from sqlalchemy import func
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=100)

    def __repr__(self):
        return f'Item {self.username}'

    @property
    def password(self):
        return self.password

    # encrypt password field
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    @classmethod
    def username_exists(cls, username):
        existing_user = cls.query.filter_by(username=username).first()
        return existing_user is not None

    @classmethod
    def email_exists(cls, email):
        existing_user = cls.query.filter_by(email=email).first()
        return existing_user is not None


class Question(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    question = db.Column(db.String(), nullable=False)
    points = db.Column(db.Integer(), nullable=False, default=5)
    answer_id = db.Column(db.Integer(), db.ForeignKey('answer.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

    @property
    def answer(self):
        return Answer.query.get(self.answer_id).answer

    @property
    def topic(self):
        return f'#{Topic.query.get(self.topic_id).topic}'

    @classmethod
    def save_question(cls, data):
        Answer.save_answer(data['answer'])
        answer_id = db.session.query(func.max(Answer.id)).scalar()
        new_question = Question(
            question=data['question'],
            points=data['points'],
            topic_id=data['topic'],
            answer_id=answer_id
        )
        db.session.add(new_question)
        db.session.commit()


class Answer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    answer = db.Column(db.String(1000), nullable=False)
    #questions = db.relationship('Question', backref='answer')

    @classmethod
    def save_answer(cls, ans):
        new_answer = Answer(answer=ans)
        db.session.add(new_answer)
        db.session.commit()


class Topic(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    topic = db.Column(db.String(60), nullable=False)
    #questions = db.relationship('Question', backref='topic')

    @classmethod
    def save_topic(cls, topic):
        new_topic = Topic(topic=topic)
        db.session.add(new_topic)
        db.session.commit()

# class Image(db.Model):