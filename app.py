from flask import Flask, request, Response, jsonify
from dotenv import load_dotenv
import os
import googlemaps

load_dotenv(".env")
API_KEY = os.getenv("google_map_key")

app = Flask(__name__)

# Define client
gmaps = googlemaps.Client(key=API_KEY)

# Geocode a zipcode
geocode_result = gmaps.geocode("97124")
lat = geocode_result[0]["geometry"]["location"]["lat"]
lon = geocode_result[0]["geometry"]["location"]["lng"]
geocode_loc = (lat, lon)

# Define search for parks
parks_result = gmaps.places_nearby(
    location=geocode_loc, radius=2000, open_now=False, type="park"
)


@app.route("/")
def root():
    return {"message": "Server is running!"}


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


@app.route("/parks", methods=["GET", "POST"])
def parks():
    json_data = request.get_json()

    # Geocode a zipcode
    geocode_results = gmaps.geocode(json_data["postal_code"])
    lats = geocode_results[0]["geometry"]["location"]["lat"]
    lons = geocode_results[0]["geometry"]["location"]["lng"]
    geocode_location = (lats, lons)

    # Define search for parks
    park_results = gmaps.places_nearby(
        location=geocode_location, radius=4000, open_now=False, type="park"
    )

    resp = Response(park_results)
    resp.status_code = 200

    park_data = []

    for park in park_results["results"]:
        try:
            parks = {
                "name": park["name"],
                "address": park["vicinity"],
                "rating": park["rating"],
                "photo_ref": park["photos"][0]["photo_reference"],
                "key": API_KEY,
            }
        except KeyError:
            parks["rating"] = None

        park_data.append(parks)
        unique_park_data = [
            dict(tupleized)
            for tupleized in set(tuple(item.items()) for item in park_data)
        ]

    return jsonify(unique_park_data)


if __name__ == "__main__":
    print("parks-api")
    app.run(host="0.0.0.0", port=80, debug=True, use_reloader=True)
