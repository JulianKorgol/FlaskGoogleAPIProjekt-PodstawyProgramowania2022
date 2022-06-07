from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from googleapi import GoogleMaps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projekt.db'

db = SQLAlchemy(app)

class Coordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CoordinateA = db.Column(db.String(20), nullable=False)
    CoordinateB = db.Column(db.String(20), nullable=False)

class Distance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CoordinatesStart = db.Column(db.Integer, nullable=False)
    CoordinatesEnd = db.Column(db.Integer, nullable=False)
    DistanceFromPoints = db.Column(db.String(20), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lenghtCoordinates = int(request.form['allOfTheCoordinates'])

        for i in range(1, lenghtCoordinates+1, 2):
            firstCoordinate = request.form['kordynaty' + str(i)]

            secondCoordinatei = i+1
            secondCoordinate = request.form['kordynaty' + str(secondCoordinatei)]

            coordinateToSQL = Coordinates(CoordinateA=firstCoordinate, CoordinateB=secondCoordinate)

            db.session.add(coordinateToSQL)
            db.session.commit()
        return redirect('http://localhost:5000/show', code=302)
    else:
        return render_template("index.html")

@app.route('/show', methods=['GET'])
def show():
    koordynaty = Coordinates.query.all()

    for k in koordynaty:
        for i in koordynaty:
            if i != k:
                Coordinate1 = str(k.CoordinateA) + ',' + str(k.CoordinateB)
                Coordinate2 = str(i.CoordinateA) + ',' + str(k.CoordinateB)
                odlegloscPunktowa = int(GoogleMaps(Coordinate1, Coordinate2))
                toSQL = Distance(CoordinatesStart=Coordinate1, CoordinatesEnd=Coordinate2, DistanceFromPoints=odlegloscPunktowa)
                db.session.add(toSQL)
                db.session.commit()

    return render_template("show.html")

if __name__ == "__main__":
    app.run(debug=True)
