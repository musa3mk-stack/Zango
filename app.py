from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TERMII_KEY = os.environ.get("TERMII_KEY")
print("==================================")
print("KEY LOADED:", TERMII_KEY) # Dole sai mu ga tlv_u... a logs
print("==================================")

@app.route("/")
def home():
    return {"status": "running", "key_exists": bool(TERMII_KEY)}

@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    phone = request.json.get("phone")
    print("PHONE:", phone, "KEY:", TERMII_KEY[:5] if TERMII_KEY else "NONE")
    
    url = "https://api.ng.termii.com/api/sms/otp/send"
    payload = {
        "api_key": TERMII_KEY,
        "to": phone,
        "from": "Zango",
        "sms": "Zango code < 1234 >",
        "channel": "generic",
        "pin_time_to_live": 5,
        "pin_length": 4,
        "message_type": "NUMERIC"
    }
    r = requests.post(url, json=payload)
    print("TERMII RESPONSE:", r.json()) # Wannan zai nuna mana kuskuren Termii
    return jsonify(r.json())
