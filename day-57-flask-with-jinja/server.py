from flask import Flask, render_template
from datetime import datetime
import requests
import random

current_year = datetime.now().year

app = Flask(__name__)

@app.route("/")
def main():
    random_number = random.randint(1, 10)
    return render_template("index.html", year=current_year, rand_num=random_number)

@app.route("/guess/<name>")
def to_guess(name):
    url_age = "https://api.agify.io"
    url_gender = "https://api.genderize.io"
    params = {"name": name.title()}
    agify = requests.get(url=url_age, params=params).json()
    age = agify["age"]
    genderize = requests.get(url=url_gender, params=params).json()
    gender = genderize["gender"]
    return render_template("guess.html", name=name.title(), age=age, gender=gender, year=current_year)

@app.route("/blog/<num>")
def to_blog(num):
    print(num)
    blog_url = "https://api.npoint.io/4358ffbd346683abf0e4"
    all_posts = requests.get(blog_url).json()
    return render_template("blog.html", posts=all_posts)

if __name__ == "__main__":
    app.run(debug=True)
