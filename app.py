from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError
from json import loads
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://fhywgmas:wRqHwWx03uduz1cfzXAq97D34bVlGfgC@ziggy.db.elephantsql.com:5432/fhywgmas"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

profile = {
    "success": True,
    "data":{"last_updated": "2/3/2021, 8:48:51 PM", 
            "username": "Jimmy_Woo",
            "role": "Engineer",
            "color": "green"
            }
}


class Tank(db.Model):
    __tablename__ = 'tanks'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), unique=True, nullable=False)
    lat = db.Column(db.String(50), nullable=False)
    long = db.Column(db.String(50), nullable=False)
    percentage_full = db.Column(db.Integer, nullable=False)

class TankSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tank
        fields = ("id","location","lat","long","percentage_full")

db.init_app(app)
migrate = Migrate(app, db)  

@app.route("/")
def home():
    return "Hello There"

@app.route("/profile", methods=["GET"])
def get_profile():
    return jsonify(profile)


@app.route("/profile", methods=["POST"])
def post_profile():
    profile["data"]["last_updated"] = datetime.now()
    profile["data"]["username"] = request.json["username"]
    profile["data"]["role"] = request.json["role"]
    profile["data"]["color"] = request.json["color"]
   
    
    return profile

@app.route("/profile", methods=["PATCH"])
def update_profile():
    if "username" in request.json:
        profile["data"]["username"] = request.json["username"]
  
    if "role" in request.json:
        profile["data"]["role"] = request.json["role"]

    if "color" in request.json:
        profile["data"]["color"] = request.json["color"]
  
    profile["data"]["last_updated"] = datetime.now()

    return profile

#GET /data
@app.route("/data", methods=["GET"])
def get_tank():
    tank_w = Tank.query.all()
    tank_list = TankSchema(many=True).dump(tank_w)

    return jsonify(tank_list)


@app.route("/data", methods=["POST"])
def add_tank():
 newTank = Tank(
    location = request.json["location"],
    lat = request.json["lat"],
    long = request.json["long"],
    percentage_full =  request.json["percentage_full"]
    )
 db.session.add(newTank)
 db.session.commit()
 return TankSchema().dump(newTank)

@app.route("/data/<int:id>", methods=["PATCH"])
def update_dish(id):
  tank_w = Tank.query.get(id)
  update = request.json

  if "location" in update:
    tank_w.location = update["location"]
  if "lat" in update:
    tank_w.lat = update["lat"]
  if "long" in update:
    tank_w.long = update["long"]
  if "percentage_full" in update:
    tank_w.percentage_full = update["percentage_full"]
  db.session.commit()
  return TankSchema().dump(tank_w)
@app.route("/data/<int:id>", methods=["DELETE"])
def delete_tank(id):
    tank = Tank.query.get(id)
    db.session.delete(tank)
    db.session.commit()

    return {
  "success": True
   }

if __name__ == '__main__':
    app.run(debug=True)
