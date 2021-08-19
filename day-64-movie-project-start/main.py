from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy, SessionBase
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextField
from wtforms.validators import DataRequired
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somesecretkey'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
TMDB_SEARCH_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAIL_ENDPOINT = "https://api.themoviedb.org/3/movie/"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
POSTER_PATH = "https://image.tmdb.org/t/p/original"
params = {
    "api_key": TMDB_API_KEY,
}


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.Text)
    img_url = db.Column(db.String(300), nullable=False)

###### create/delete database
db.create_all()
# db.drop_all()


class EditForm(FlaskForm):
    rating = FloatField("Rating", validators=[DataRequired()])
    review = TextField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    total_movies = len(all_movies)
    bottom_rank = total_movies
    for movie in all_movies:
        movie.ranking = bottom_rank
        bottom_rank -= 1
    db.session.commit()
    return render_template("index.html", movies=all_movies, total_movies=total_movies)

@app.route("/edit", methods=["POST", "GET"])
def edit():
    form = EditForm()
    if request.args.get("movie"):
        movie = eval(request.args.get("movie"))
        id = movie["id"]
        detail_endpoint = f"{TMDB_DETAIL_ENDPOINT}{movie['id']}"
        response = requests.get(url=detail_endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        title = data["title"]
        img_url = POSTER_PATH + data["poster_path"]
        year = data["release_date"]
        description = data["overview"]
        movie_to_save = Movie(id=id, title=title, year=year, description=description, rating=None, ranking=None,
                              review="None", img_url=img_url)
        db.session.add(movie_to_save)
        db.session.commit()
        return render_template("edit.html", form=form, id=id)
    if request.method == "POST":
        id = request.args.get("id")
        movie_to_edit = Movie.query.get(id)
        movie_to_edit.rating = form.rating.data
        movie_to_edit.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    id = request.args.get("id")
    return render_template("edit.html", form=form, id=id)


@app.route("/delete/<int:id>")
def delete(id):
    movie_to_delete = Movie.query.get(id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["POST", "GET"])
def add():
    form = AddForm()
    if request.method == "POST":
        title = request.form["title"]
        params["query"] = title
        response = requests.get(url=TMDB_SEARCH_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        movie_list = data["results"]
        total_movie = len(movie_list)
        return render_template("select.html", movie_list=movie_list, total_movie=total_movie)
    return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
