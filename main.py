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


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/addpost", methods=["POST", "GET"])
def addpost():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]

        post = Riley_blog(
            title=title, author=author, content=content, post_date=datetime.now()
        )

        db.session.add(post)
        db.session.commit()
        print("Done")

        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/update/<int:id", methods=["POST", "GET"])
@login_required
def update(id):
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]
        print(content)

        post = Riley_blog.query.filter_by(id=id).first()

        post.title = title
        post.author = author
        post.content = content

        db.session.add(post)
        db.session.commit()
        return redirect("/")

    edit = Riley_blog.query.filter_by(id=id).first()

    return render_template("update.html", edit=edit)


@app.route("/delete/<int: id>")
@login_required
def delete(id):
    data = Riley_blog.query.filter_by(id=id).first()

    db.session.delete(data)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        print("login")
        username = request.form("username")
        password = request.form("password")
        user = User.query.filter_by(username=username).first()

        if not user and not check_password_hash(user.password, password):
            flash("Wrong username/password :skull:")

            return render_template("not.html")
    else:
        login_user(user)

        print("Successfully logged in")
        return redirect(url_for("index.html"))

    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        print("Attempt to sign up!")
        username = request.form("username")
        password = request.form("password")

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("signup.html")


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    login_user()

    return redirect(url_for("index"))


# main driver function
if __name__ == "__main__":
    app.run(debug=True)
