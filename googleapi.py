import googlemaps as googlemaps

def GoogleMaps(CoordinateA, CoordinateB):
    API_KEY = "KEYHERE";

    client = googlemaps.Client(API_KEY)
    directions_result = client.directions(origin=CoordinateA, destination=CoordinateB, mode="driving", avoid="ferries")

    return directions_result[0]['legs'][0]['distance']['value']
