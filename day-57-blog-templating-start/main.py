from flask import Flask, render_template
import requests
from post import Post
from datetime import datetime

current_year = datetime.now().year
all_objects = []
blog_url = "https://api.npoint.io/4358ffbd346683abf0e4"
all_posts = requests.get(blog_url).json()
for post in all_posts:
    post_object = Post(post_id=post["id"], post_title=post["title"], post_subtitle=post["subtitle"], post_body=post["body"])
    all_objects.append(post_object)


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", posts=all_objects, year=current_year)


@app.route("/post/<int:num>")
def to_post(num):
    return render_template("post.html", posts=all_posts, num=num, year=current_year)

if __name__ == "__main__":
    app.run(debug=True)
