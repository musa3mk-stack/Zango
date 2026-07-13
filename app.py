from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app) 

# An gyara sunan variable zuwa TERMII_API_KEY don ya dace da Render
TERMII_KEY = os.environ.get("TERMII_API_KEY") 

@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    data = request.json
    phone = data.get("phone") 
    
    if not phone:
        return jsonify({"error": "Phone is required"}), 400

    # Sauya 080... zuwa 23480...
    if phone.startswith("0"):
        phone = "234" + phone[1:]
    elif phone.startswith("+234"):
        phone = phone[1:]
    
    # Tabbatar cewa akwai API Key kafin a tura
    if not TERMII_KEY:
        return jsonify({"error": "Internal Server Error: API Key not configured"}), 500

    url = "https://api.ng.termii.com/api/sms/otp/send"
    payload = {
        "api_key": TERMII_KEY, 
        "to": phone,
        "from": "Zango", 
        "sms": "Your Zango code is < 1234 >",
        "channel": "generic",
        "pin_time_to_live": 5,
        "pin_length": 4,
        "message_type": "NUMERIC"
    }
    
    print(f"Sending to Termii: {phone}") 
    try:
        r = requests.post(url, json=payload)
        print(f"TERMII SAYS: {r.text}")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Zango Backend is Running"

if __name__ == "__main__":
    app.run(debug=True)
