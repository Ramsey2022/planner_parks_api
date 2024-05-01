from flask import Flask, request, abort, Response, jsonify, render_template
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


@app.route("/parkjson")
def parkjson():
    return jsonify(parks_result)


@app.route("/parks", methods=["GET"])
def parks():
    # zip = request.args.get("zip")

    # if zip is None:
    # abort(400, "Missing zipcode argument")

    # Geocode a zipcode
    geocode_results = gmaps.geocode("97124")
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
            }
        except KeyError:
            park["rating"] = None

        park_data.append(parks)

    return render_template(
        "index.html",
        title="Nearby Parks",
        park_data=park_data,
        API_KEY=(API_KEY),
    )


if __name__ == "__main__":
    print("parks-api")
    app.run(host="0.0.0.0", port=80, debug=True, use_reloader=True)
