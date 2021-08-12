from flask import Flask, render_template
import requests
from datetime import datetime

current_year = datetime.now().year

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("/contact.html")

if __name__ == "__main__":
    app.run(debug=True)

