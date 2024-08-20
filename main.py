from flask import Flask, render_template, request, redirect, url_for
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import flash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite://blogs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "sigmaskibidigyattohiomewing"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Riley_blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(20))
    post_date = db.Column(db.DateTime)
    content = db.Column(db.text)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False)


@app.route("/")
def index():
    article = Riley_blog.query.order_by(Riley_blog.post_date.desc()).all()
    print(current_user.is_anonymous)
    if current_user.is_anonymous:
        name = "quest"
    else:
        name = current_user.username
        print("Success!!!")

    return render_template("index.html", article=article, name=name)
