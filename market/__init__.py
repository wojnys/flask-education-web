from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os, tempfile

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"  # flask locate DATABASE + DB.name
app.config['SECRET_KEY'] = 'd7436f2b4bfd9aa88a49d2dc'
# app.config['UPLOADED_PHOTOS_DEST'] = '/static/uploads'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(APP_ROOT, 'uploads')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)  # database
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)


with app.app_context():
    db.create_all()
    db.drop_all()


from market.models import *

admin = Admin(app, name='Admin panel', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Answer, db.session))
admin.add_view(ModelView(Topic, db.session))

from market import routes
