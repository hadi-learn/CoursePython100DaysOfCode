from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return render_template("login.html", username=username, password=password)
    else:
        return "get get"


if __name__ == "__main__":
    app.run(debug=True)
