from flask import Flask, jsonify, render_template, request, make_response
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
@app.route("/random", methods=["GET"])
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
    # random_cafe_json_3 = jsonify(cafe=random_cafe_2.to_dict())
    # return random_cafe_json
    return random_cafe_json_2
    # return random_cafe_json_3


@app.route("/all", methods=["GET"])
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


@app.route("/search", methods=["GET"])
def search():
    location = request.args.get("location")
    cafes_query = db.session.query(Cafe).filter_by(location=location).all()
    if cafes_query:
        print(cafes_query)
        print(type(cafes_query))
        all_cafes = []
        for cafe in cafes_query:
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
        all_location_json = jsonify(cafe=all_cafes)
        return all_location_json
    else:
        not_found = {
            "Not Found": f"Sorry, we don't have a cafe at location: {location}"
        }
        not_found_json = jsonify(error=not_found)
        return make_response(not_found_json, 404)

## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    map_url = request.form.get("map_url")
    img_url = request.form.get("img_url")
    location = request.form.get("location")
    seats = request.form.get("seats")
    has_toilet = True if request.form.get("has_toilet") == "1" else False
    has_wifi = True if request.form.get("has_wifi") == "1" else False
    has_sockets = True if request.form.get("has_sockets") == "1" else False
    can_take_calls = True if request.form.get("can_take_calls") == "1" else False
    coffee_price = request.form.get("coffee_price")
    cafe_to_add = Cafe(name=name, map_url=map_url, img_url=img_url, location=location, seats=seats,
                       has_toilet=has_toilet, has_wifi=has_wifi, has_sockets=has_sockets,
                       can_take_calls=can_take_calls, coffee_price=coffee_price)
    try:
        db.session.add(cafe_to_add)
        db.session.commit()
        feedback = {"success": "Sucessfully added the new cafe."}
        response = 200
    except:
        feedback = {"failed": "Something went wrong."}
        response = 400
    finally:
        feedback_json = jsonify(response=feedback)
        return make_response(feedback_json, response)


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:id>", methods={"PATCH"})
def update(id):
    new_price = request.args.get("new_price")
    try:
        cafe_to_update = db.session.query(Cafe).get(id)
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        feedback = {"Success": f"Successfully updated the price to cafe with id: {id}."}
        response = 200
    except:
        feedback = {"Failed": f"Sorry, a cafe with id: {id} not found in our database."}
        response = 404
    finally:
        return make_response(jsonify(feedback), response)

## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:id>", methods=["DELETE"])
def delete(id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        try:
            cafe_to_delete = db.session.query(Cafe).get(id)
            db.session.delete(cafe_to_delete)
            db.session.commit()
            feedback = {"Success": f"Successfully deleted the cafe with id: {id}."}
            response = 200
        except:
            feedback = {"Failed": f"Sorry, a cafe with id: {id} not found in our database."}
            response = 404
        finally:
            return make_response(jsonify(feedback), response)
    else:
        feedback = {"Error": "Sorry that's not allowed, make sure you have the correct API KEY"}
    return make_response(jsonify(feedback), 403)


@app.route("/test/<int:id>", methods=["PATCH"])
def test(id):
    new_price = request.args.get("new_price")
    print(new_price)
    return "Test"

if __name__ == '__main__':
    app.run(debug=True)
