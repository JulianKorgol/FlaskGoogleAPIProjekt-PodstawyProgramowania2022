from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from googleapi import GoogleMaps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projekt.db'

db = SQLAlchemy(app)

class Coordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Coordinates = db.Column(db.String(50), nullable=False)

class Distance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CoordinatesA = db.Column(db.Integer, db.ForeignKey(Coordinates.id), nullable=False)
    CoordinatesB = db.Column(db.Integer, db.ForeignKey(Coordinates.id), nullable=False)
    DistanceFromPoints = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        firstCoordinate = request.form['kordynaty1']
        secondCoordinate = request.form['kordynaty2']
        CoordinatesToSql = firstCoordinate + ',' + secondCoordinate

        uploadToSQL = Coordinates(Coordinates=CoordinatesToSql)

        db.session.add(uploadToSQL)
        db.session.commit()
        return redirect('http://localhost:5000/', code=302)
    else:
        coordinate = Coordinates.query.order_by(Coordinates.id).all()

        return render_template("index.html", coordinates=coordinate)

@app.route('/show', methods=['GET'])
def show():
    koordynaty = Coordinates.query.all()


    # Każdy z każdym [kordynaty]
    for k in koordynaty:
        for i in koordynaty:
            if i != k:
                Coordinate1 = k.Coordinates
                Coordinate2 = i.Coordinates
                odlegloscPunktowa = int(GoogleMaps(Coordinate1, Coordinate2))
                toSQL = Distance(CoordinatesA=k.id, CoordinatesB=i.id, DistanceFromPoints=odlegloscPunktowa)
                db.session.add(toSQL)
                db.session.commit()

    # Algorytm najbliższych sąsiadów
    def first(collection):
        return next(iter(collection))

    def distance(a, b, roads):
        for r in roads:
            if a.id == r.CoordinatesA and b.id == r.CoordinatesB:
                return r.DistanceFromPoints

    def nearest_neighbour(a, points):
        return min(points, key=lambda c: distance(c, a, roads))

    def nn_tour(points):
        start = first(points)
        tour = [start]
        unvisited = set(points - {start})
        while unvisited:
            c = nearest_neighbour(tour[-1], unvisited)
            tour.append(c)
            unvisited.remove(c)
        return tour

    # Wywołanie algorytmu
    points = set(Coordinates.query.all())
    roads = Distance.query.all()
    theFastestWay = []

    for n in nn_tour(points):
        theFastestWay.append(n)

    # Przygotowujemy link
    googleLink = "https://www.google.pl/maps/dir/"
    for x in theFastestWay:
        googleLink += x.Coordinates + "/"

    Distance.query.delete()
    db.session.commit()
    return render_template("show.html", googleLink=googleLink)

@app.route('/deleteAll', methods=['POST'])
def deleteCoordinates():
    Coordinates.query.delete()
    Distance.query.delete()
    db.session.commit()
    return redirect('http://localhost:5000/', code=302)

if __name__ == "__main__":
    app.run(debug=True)
