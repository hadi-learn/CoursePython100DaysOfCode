from flask import Flask

app = Flask(__name__)

def make_bold(function):
    def wrapper_function():
        return f'<b>{function()}</b>'
    return wrapper_function

def make_emphasis(function):
    def wrapper_function():
        return f'<em>{function()}</em>'
    return wrapper_function

def make_underlined(function):
    def wrapper_function():
        return f'<u>{function()}</u>'
    return wrapper_function


@app.route('/')
def hello_world():
    return '<h1 style="text-align: center">Hello, World!</h1>' \
           '<p>This is a paragraph</p>' \
           '<img src="https://media.giphy.com/media/JbYxlLwcd7O6I/giphy.gif" alt="heading-image" width=200>'


@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "Bye"


@app.route("/username/<name>/<int:number>")  # convert variable number's type to integer
def greet(name, number):
    return f"Hello there {name}, you are {number} years old"


if __name__ == "__main__":
    # run the app in debug mode for auto reload
    app.run(debug=True)
