from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from random import randint
import json

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random")
def random():
    rows = Cafe.query.count()
    random_id = randint(1, rows)
    random_cafe = Cafe.query.get(random_id)
    random_cafe_json = jsonify(id=random_cafe.id, name=random_cafe.name, map_url=random_cafe.map_url,
                               img_url=random_cafe.img_url, location=random_cafe.location, seats=random_cafe.seats,
                               has_toilet=random_cafe.has_toilet, has_wifi=random_cafe.has_wifi,
                               has_sockets=random_cafe.has_sockets, can_take_calls=random_cafe.can_take_calls,
                               coffee_price=random_cafe.coffee_price)
    random_cafe_2 = db.session.query(Cafe).order_by(func.random()).first()
    random_cafe_json_2 = jsonify(
        cafe={
        "id": random_cafe_2.id,
        "name": random_cafe_2.name,
        "map_url": random_cafe_2.map_url,
        "img_url": random_cafe_2.img_url,
        "location": random_cafe_2.location,
        "seats": random_cafe_2.seats,
        "has_toilet": random_cafe_2.has_toilet,
        "has_wifi": random_cafe_2.has_wifi,
        "has_sockets": random_cafe_2.has_sockets,
        "can_take_calls": random_cafe_2.can_take_calls,
        "coffee_price": random_cafe_2.coffee_price,
    }
    )
    # return random_cafe_json
    return random_cafe_json_2


@app.route("/all")
def all():
    all_cafes_query = db.session.query(Cafe).all()
    all_cafes = []
    for cafe in all_cafes_query:
        item = {
        "id": cafe.id,
        "name": cafe.name,
        "map_url": cafe.map_url,
        "img_url": cafe.img_url,
        "location": cafe.location,
        "seats": cafe.seats,
        "has_toilet": cafe.has_toilet,
        "has_wifi": cafe.has_wifi,
        "has_sockets": cafe.has_sockets,
        "can_take_calls": cafe.can_take_calls,
        "coffee_price": cafe.coffee_price,
        }
        all_cafes.append(item)
    all_cafes_json = jsonify(cafe=all_cafes)
    return all_cafes_json


## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
