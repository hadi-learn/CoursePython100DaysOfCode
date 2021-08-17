from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somesecretkey'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location URL', validators=[DataRequired(), URL()])
    open_time = StringField('Open', validators=[DataRequired()])
    closing_time = StringField('Close', validators=[DataRequired()])
    coffee_rating = SelectField(u'Coffee', choices=[('x', 'not_available'), ('*', 'very_bad'), ('**', 'bad'),
                                                   ('***', 'average'), ('****', 'good'), ('*****', 'very_good')],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi', choices=[('x', 'not_available'), ('*', 'very_bad'), ('**', 'bad'),
                                               ('***', 'average'), ('****', 'good'), ('*****', 'very_good')],
                              validators=[DataRequired()])
    power_rating = SelectField('Power', choices=[('x', 'not_available'), ('*', 'very_bad'), ('**', 'bad'),
                                                 ('***', 'average'), ('****', 'good'), ('*****', 'very_good')],
                               validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    # form.coffee_rating.choices = [a.id for a in Coffee.query.order_by]
    if form.validate_on_submit():
        print("True")
        new_cafe = form.cafe.data + "," + form.location.data + "," + form.open_time.data + "," + form.closing_time.data + "," + form.coffee_rating.data + "," + form.wifi_rating.data + "," + form.power_rating.data
        with open("cafe-data.csv", mode="a") as csv_file:
            csv_file.write("\n" + new_cafe)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        total_cafe = len(list_of_rows)
        total_aspect = len(list_of_rows[0])
    return render_template('cafes.html', cafes=list_of_rows, total_cafe=total_cafe, total_aspect=total_aspect)


if __name__ == '__main__':
    app.run(debug=True)
