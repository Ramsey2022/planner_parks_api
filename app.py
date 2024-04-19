from flask import Flask, request, abort, Response, jsonify
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
    location=geocode_loc, radius=20000, open_now=False, type="park"
)


@app.route("/")
def root():
    return {"message": "Server is running!"}


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


@app.route("/parks")
def parks():
    return jsonify(parks_result)


if __name__ == "__main__":
    print("parks-api")
    app.run(host="0.0.0.0", port=80, debug=True, use_reloader=True)
