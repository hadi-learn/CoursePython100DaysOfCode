from flask import Flask, render_template, request
import requests
from datetime import datetime
import calendar
from send_mail import SendMail

current_year = datetime.now().year
all_objects = []
all_date = []
all_body = []
total = len(all_objects)
blog_url = "https://api.npoint.io/4358ffbd346683abf0e4"
all_posts = requests.get(blog_url).json()
for post in all_posts:
    all_objects.append(post)
    day = post["date"].split("-")[0]
    month = calendar.month_name[int(post["date"].split("-")[1])]
    year = post["date"].split("-")[2]
    date = (day, month, year)
    all_date.append(date)
    sentences = [sentence.replace(".", "") for sentence in post["body"].split(". ")]
    all_body.append(sentences)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", posts=all_objects, date=all_date)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        send_email = SendMail(name, email, phone, message)
        send_email.send_email()
        return render_template("contact.html", data=True)
    else:
        return render_template("contact.html")


@app.route("/post/<int:num>")
def to_post(num):
    return render_template("post.html", posts=all_objects, num=num, date=all_date, bodies=all_body)


if __name__ == "__main__":
    app.run(debug=True)

