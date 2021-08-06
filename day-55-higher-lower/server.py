from flask import Flask
import random

MAIN_GIF = "https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"
CORRECT_GIF = "https://media.giphy.com/media/H6Qqxi3RsbyuCry8Ma/giphy.gif"
TOO_LOW_GIF = "https://media.giphy.com/media/5T8tEJtCgvDuo/giphy.gif"
TOO_HIGH_GIF = "https://media.giphy.com/media/nR4L10XlJcSeQ/giphy.gif"
RANDOM = random.randint(0, 9)
print(RANDOM)

app = Flask(__name__)


def guessed(function):
    def wrapper(**kwargs):
        if kwargs["number"] == RANDOM:
            return f'<h1 style="color: green">You found me! {function(kwargs["number"])} ' \
                   f'is the correct answer.</h1>' \
                   f'<img src="{CORRECT_GIF}" alt="correct-image" width=500>'
        elif kwargs["number"] < RANDOM:
            return f'<h1 style="color: blue">Too low, try again! {function(kwargs["number"])} ' \
                   f'not the correct answer.</h1>' \
                   f'<img src="{TOO_LOW_GIF}" alt="too-low-image" width=500>'
        else:
            return f'<h1 style="color: red">Too high, try again! {function(kwargs["number"])} ' \
                   f'not the correct answer.</h1>' \
                   f'<img src="{TOO_HIGH_GIF}" alt="too-high-image" width=500>'

    return wrapper


@app.route("/")
def home():
    return f'<h1>Guess a number between 0 and 9</h1>' \
           f'<img src={MAIN_GIF} alt="heading-image" width=500>'


@app.route("/<int:number>")
@guessed
def guess_number(number):
    return f"{number}"


if __name__ == "__main__":
    app.run(debug=True)
