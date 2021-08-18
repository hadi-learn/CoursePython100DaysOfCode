from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somesecretkey'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # year = db.Column(db.DateTime, nullable=False)
    year = db.Column(db.String(4), nullable=False)
    # year = db.Column(db.String(min=4, max=4), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(300), nullable=False)

###### create/delete database
db.create_all()
# db.drop_all()

###### delete records manually
# movie_id = 1
# movie_to_delete = Movie.query.get(movie_id)
# db.session.delete(movie_to_delete)


###### add records to database manually
# new_movie = Movie(title="Phone Booth",
#                   year="2002",
#                   description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#                   rating=7.3, ranking=10, review="My favourite character was the caller.",
#                   img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
# db.session.add(new_movie)
# db.session.commit()

class EditForm(FlaskForm):
    rating = FloatField("Rating", validators=[DataRequired()])
    review = TextField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def home():
    all_movies = Movie.query.all()
    total_movies = len(all_movies)
    return render_template("index.html", movies=all_movies, total_movies=total_movies)

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    form = EditForm()
    # movie_to_edit = Movie.query.get(id)
    # rating = movie_to_edit.rating
    # review = movie_to_edit.review
    if request.method == "POST":
        movie_to_edit = Movie.query.get(id)
        movie_to_edit.rating = form.rating.data
        movie_to_edit.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, id=id)


if __name__ == '__main__':
    app.run(debug=True)
