from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
import time


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)
    # return "OK"


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = db.session.query(BlogPost).get(index)
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    edit = False
    if request.method == "POST":
        if form.validate_on_submit():
            now = time.time()
            date = datetime.fromtimestamp(now).strftime("%B %d, %Y")
            title = form.title.data
            subtitle = form.subtitle.data
            author = form.author.data
            img_url = form.img_url.data
            body = form.body.data
            blog_to_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                date=date,
                author=form.author.data,
                img_url=form.img_url.data,
                body=form.body.data
            )
            db.session.add(blog_to_post)
            db.session.commit()
            return redirect(url_for("get_all_posts"))
        return render_template("make-post.html", form=form, edit=edit)
    else:
        return render_template("make-post.html", form=form, edit=edit)


@app.route("/edit/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    blog_to_edit = db.session.query(BlogPost).get(post_id)
    edit = True
    form = CreatePostForm(
        title = blog_to_edit.title,
        subtitle = blog_to_edit.subtitle,
        author = blog_to_edit.author,
        img_url = blog_to_edit.img_url,
        body = blog_to_edit.body
    )
    if form.validate_on_submit():
        blog_to_edit.title = form.title.data
        blog_to_edit.subtitle = form.subtitle.data
        blog_to_edit.author = form.author.data
        blog_to_edit.img_url = form.img_url.data
        blog_to_edit.body = form.body.data
        db.session.commit()
        return redirect(url_for("show_post", index=post_id))
    return render_template("make-post.html", form=form, edit=edit)
    # return "OK"


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/delete")
def delete():
    post_id = request.args.get("post_id")
    post_to_delete = db.session.query(BlogPost).get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)