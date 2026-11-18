from flask import Flask, jsonify

app = Flask(__name__)
ROOMS = [{"id": 1, "type": "deluxe", "free": 4}, {"id": 2, "type": "suite", "free": 1}]

@app.get("/rooms")
def rooms():
    return jsonify(ROOMS)

@app.get("/health")
def health():
    return "ok", 200
