from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Wannan zai bari React din ya iya kira backend

# Karanta API Key daga Render Environment Variables
TERMII_KEY = os.environ.get("TERMII_KEY")

@app.route("/")
def home():
    return jsonify({
        "status": "Zango Backend is running ✅",
        "message": "Yi amfani da /api/send-otp da /api/verify-otp"
    })

@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    try:
        data = request.json
        phone = data.get("phone")

        if not phone:
            return jsonify({"error": "Phone number is required"}), 400

        # Tsaftace number: 080... -> 23480...
        if phone.startswith("0"):
            phone = "234" + phone[1:]
        
        payload = {
            "api_key": TERMII_KEY,
            "message_type": "NUMERIC",
            "to": phone,
            "from": "Zango",
            "channel": "dnd",
            "pin_attempts": 3,
            "pin_length": 4,
            "pin_placeholder": "< 1234 >",
            "message_text": "Zango code: < 1234 >. Kada ka baiwa kowa.",
            "pin_type": "NUMERIC"
        }
        
        r = requests.post("https://api.ng.termii.com/api/sms/otp/send", json=payload)
        return jsonify(r.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():
    try:
        data = request.json
        payload = {
            "api_key": TERMII_KEY,
            "pin_id": data.get("pin_id"),
            "pin": data.get("pin")
        }
        
        r = requests.post("https://api.ng.termii.com/api/sms/otp/verify", json=payload)
        return jsonify(r.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
