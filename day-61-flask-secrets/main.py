from flask import Flask, render_template, request
from login import LoginForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = "testkey"
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data_email = form.email.data
        data_password = form.password.data
        if data_email == "admin@email.com" and data_password == "12345678":
            return render_template("success.html")
        return render_template("denied.html")
    return render_template("login.html", form=form)


@app.route("/test", methods=["POST", "GET"])
def test():
    form = LoginForm()
    if form.validate_on_submit():
        data_email = form.email.data
        data_password = form.password.data
        if data_email == "admin@email.com" and data_password == "12345678":
            return render_template("success.html")
        return render_template("denied.html")
    return render_template("test.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)