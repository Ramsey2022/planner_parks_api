from flask import Flask, request, abort, Response, jsonify

app = Flask(__name__)


@app.route("/")
def root():
    return {"message": "Server is running!"}


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


if __name__ == "__main__":
    print("parks-api")
    app.run(host="0.0.0.0", port=80, debug=True, use_reloader=True)
