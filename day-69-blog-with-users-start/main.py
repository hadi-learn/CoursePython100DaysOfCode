from flask import Flask, render_template, redirect, url_for, flash, request, g, abort, jsonify
from functools import wraps
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##Initiate Flask LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

##Declare the base of relational database
Base = declarative_base()

##Gravatar initialization
gravatar = Gravatar(
    app=app,
    size=100,
    rating="g",
    default="retro",
    force_default=False,
    force_lower=False
)

##CONFIGURE TABLES
class User(UserMixin, db.Model, Base):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    ## Try to add editor section on each post
    # editor = relationship("Editor", back_populates="author")


class BlogPost(db.Model, Base):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author = relationship("User", back_populates="posts")
    date = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    comments = relationship("Comment", back_populates="blog")
    last_edited_date = db.Column(db.String(250))
    author_id = db.Column(db.Integer, ForeignKey("user.id"))
    ## Try to enable editor section
    # editor = relationship("Editor", back_populates="blog")



class Comment(db.Model, Base):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(1000), nullable=False)
    author = relationship("User", back_populates="comments")
    author_id = db.Column(db.Integer, ForeignKey("user.id"))
    blog = relationship("BlogPost", back_populates="comments")
    blog_id = db.Column(db.Integer, ForeignKey("blog_posts.id"))


## TRY TO ADD EDITOR SECTION ON EVERY POST PAGE
# class Editor(db.Model, Base):
#     __tablename__ = "comment"
#     id = db.Column(db.Integer, primary_key=True)
#     author = relationship("User", back_populates="editor")
#     author_id = db.Column(db.Integer, ForeignKey("user.id"))
#     blog = relationship("BlogPost", back_populates="editor")
#     blog_id = db.Column(db.Integer, ForeignKey("blog_posts.id"))


##CREATE TABLE ONCE
# db.create_all()


def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.get_id() == "1":
            return function(*args, **kwargs)
        else:
            abort(403,
                  description="Sorry, authorized personnel only. You don't have the permission to access this page.")
    return wrapper


def blog_owner(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        requested_post = BlogPost.query.get(kwargs["post_id"])
        owner = True if requested_post.author.id == int(current_user.get_id()) else False
        admin = True if current_user.get_id() == "1" else False
        if admin or owner:
            return function(*args, **kwargs)
        else:
            abort(403,
                  description="Sorry, authorized personnel only. You don't have the permission to access this page.")
    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    posts = BlogPost.query.all()
    admin = True if current_user.get_id() == "1" else False
    return render_template("index.html", all_posts=posts, logged_in=current_user.is_authenticated, admin=admin)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user_to_save = User(
                username = form.username.data,
                email = form.email.data,
                password = generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)
            )
            check_user_by_username = User.query.filter_by(username=form.username.data).first()
            check_user_by_email = User.query.filter_by(email=form.email.data).first()
            if check_user_by_username:
                flash("Sorry, that username already exist. Please login.")
                return redirect(url_for("login"))
            elif check_user_by_email:
                flash("Sorry, that email already exist. Please login.")
                return redirect(url_for("login"))
            else:
                db.session.add(user_to_save)
                db.session.commit()
                logout_user()
                flash("Please Login.")
                return redirect(url_for("login"))
        else:
            return render_template("register.html", form=form, logged_in=current_user.is_authenticated)
    else:
        return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user_to_login = User.query.filter_by(email=email).first()
            if user_to_login:
                if check_password_hash(pwhash=user_to_login.password, password=password):
                    login_user(user_to_login)
                    user_id = current_user.get_id()
                    # return f"Ok - user id: {user_id} - class: {type(user_id)}"
                    return redirect(url_for("home"))
                else:
                    flash("Incorrect password, please try again.")
                    return redirect(url_for("login"))
            else:
                flash("Sorry, email not found. Please try again.")
                return redirect(url_for("login"))
        else:
            return render_template("login.html", form=form, logged_in=current_user.is_authenticated)
    else:
        return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
# @login_required
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    admin = True if current_user.get_id() == "1" else False
    all_comments = []
    comment_query = Comment.query.filter_by(blog_id=post_id).all()
    for comment in comment_query:
        comment_dict = {
            "comment_text": comment.comment_text,
            "comment_author": comment.author.username,
            "comment_email": comment.author.email,
        }
        all_comments.append(comment_dict)
    if request.method == "POST":
        comment_to_save = Comment(
            comment_text = form.comment.data,
            author = current_user,
            blog = requested_post
        )
        db.session.add(comment_to_save)
        db.session.commit()
        return redirect(url_for("show_post", post_id=requested_post.id))
    return render_template("post.html", post=requested_post, logged_in=current_user.is_authenticated, admin=admin, form=form, comments=all_comments)


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route("/contact")
def contact():
    return render_template("contact.html", logged_in=current_user.is_authenticated)


@app.route("/new-post", methods=["GET", "POST"])
# ## anyone can post a new blog at this moment
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        author_name = current_user.username
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
            last_edited_date = None
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
## edit available for admin and the author
@blog_owner
@login_required
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if request.method == "POST":
        if edit_form.validate_on_submit():
            post.title = edit_form.title.data
            post.subtitle = edit_form.subtitle.data
            post.img_url = edit_form.img_url.data
            post.body = edit_form.body.data
            # add editor here if there any editor section later and delete the author line
            # post.editor = current_user
            post.author = current_user
            post.last_edited_date = date.today().strftime("%B %d, %Y")
            db.session.commit()
            return redirect(url_for("show_post", post_id=post.id))
        else:
            return render_template("make-post.html", form=edit_form, logged_in=current_user.is_authenticated,
                                   is_edit=True)
    else:
        return render_template("make-post.html", form=edit_form, logged_in=current_user.is_authenticated, is_edit=True)


@app.route("/delete/<int:post_id>")
@admin_only
@login_required
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
