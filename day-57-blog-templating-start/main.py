from flask import Flask, render_template
import requests
from datetime import datetime

current_year = datetime.now().year

app = Flask(__name__)

@app.route("/")
def home():
    blog_url = "https://api.npoint.io/4358ffbd346683abf0e4"
    all_posts = requests.get(blog_url).json()
    return render_template("index.html", posts=all_posts, year=current_year)


@app.route("/post/<int:num>")
def to_post(num):
    print(num)
    blog_url = "https://api.npoint.io/4358ffbd346683abf0e4"
    all_posts = requests.get(blog_url).json()
    return render_template("post.html", posts=all_posts, num=num, year=current_year)

if __name__ == "__main__":
    app.run(debug=True)
