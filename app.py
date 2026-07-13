from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TERMII_KEY = os.environ.get("TERMII_KEY")
TERMII_URL = "https://api.ng.termii.com/api/sms/otp/send"
TERMII_VERIFY_URL = "https://api.ng.termii.com/api/sms/otp/verify"

@app.route("/")
def home():
    return {"status": "Zango Backend is running ✅"}

@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    data = request.json
    phone = data.get("phone")
    
    payload = {
        "api_key": TERMII_KEY,
        "to": phone,
        "from": "Zango",
        "sms": "Zango code",
        "type": "plain",
        "channel": "generic",
        "pin_attempts": 3,
        "pin_time_to_live": 5,
        "pin_length": 4,
        "pin_placeholder": "< 1234 >",
        "message_type": "NUMERIC"
    }
    
    headers = {"Content-Type": "application/json"}
    res = requests.post(TERMII_URL, json=payload, headers=headers)
    return jsonify(res.json())

@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    payload = {
        "api_key": TERMII_KEY,
        "pin_id": data.get("pin_id"),
        "pin": data.get("pin")
    }
    headers = {"Content-Type": "application/json"}
    res = requests.post(TERMII_VERIFY_URL, json=payload, headers=headers)
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
