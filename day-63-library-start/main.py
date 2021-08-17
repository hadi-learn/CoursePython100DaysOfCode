from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] ="secretkeyrequired"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app=app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    #### only use this to return a particular format / content
    # def __repr__(self):
    #     return f"{self.title}"


db.create_all()


class NewBookForm(FlaskForm):
    book_name = StringField("Book", validators=[DataRequired()])
    book_author = StringField("Author", validators=[DataRequired()])
    rating = DecimalField("Rating", places=2, validators=[DataRequired()])
    submit = SubmitField("Submit")


class EditRating(FlaskForm):
    rating = DecimalField("Rating", places=2, validators=[DataRequired()])
    submit = SubmitField("Submit")


###### deleting section manually
# book_id = 1
# book_to_delete = Books.query.get(book_id)
# db.session.delete(book_to_delete)
#
# book_id = 2
# book_to_delete = Books.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()
# book_id = 3
# book_to_delete = Books.query.get(book_id)
# db.session.delete(book_to_delete)


@app.route('/')
def home():
    all_books = Books.query.all()
    total_book = len(all_books)
    return render_template("index.html", total_book=total_book, books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    form = NewBookForm()
    if request.method == "POST":
        new_book = Books(title=form.book_name.data, author=form.book_author.data, rating=form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    form = EditRating()
    book_to_edit = Books.query.get(id)
    title = book_to_edit.title
    rating = book_to_edit.rating
    if request.method == "POST":
        book_to_edit = Books.query.get(id)
        book_to_edit.rating = form.rating.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, title=title, rating=rating, id=id)


if __name__ == "__main__":
    app.run(debug=True)

