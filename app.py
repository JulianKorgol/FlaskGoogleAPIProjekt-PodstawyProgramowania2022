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
        firstCoordinate = request.form['kordynaty1']
        secondCoordinate = request.form['kordynaty2']

        coordinateToSQL = Coordinates(CoordinateA=firstCoordinate, CoordinateB=secondCoordinate)

        db.session.add(coordinateToSQL)
        db.session.commit()
        # return redirect('http://localhost:5000/show', code=302)
        return redirect('http://localhost:5000/', code=302)
    else:
        coordinate = Coordinates.query.order_by(Coordinates.id).all()
        return render_template("index.html", coordinates=coordinate)

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

@app.route('/deleteAll', methods=['POST'])
def deleteCoordinates():
    Coordinates.query.delete()
    Distance.query.delete()
    db.session.commit()
    return redirect('http://localhost:5000/', code=302)

if __name__ == "__main__":
    app.run(debug=True)
