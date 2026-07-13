from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app) # Wannan yana bawa frontend damar magana da backend

# Wannan shine zai karba daga Render Environment
TERMII_KEY = os.environ.get("TERMII_KEY") 

@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    data = request.json
    phone = data.get("phone") # Backend ya karbi phone kawai
    
    if not phone:
        return jsonify({"error": "Phone is required"}), 400

    # Sauya 080... zuwa 23480...
    if phone.startswith("0"):
        phone = "234" + phone[1:]
    elif phone.startswith("+234"):
        phone = phone[1:]
    
    url = "https://api.ng.termii.com/api/sms/otp/send"
    payload = {
        "api_key": TERMII_KEY, # Backend ne ya saka key din nan daga Render
        "to": phone,
        "from": "Zango", # Tabbatar Zango ya approved a Termii
        "sms": "Your Zango code is < 1234 >",
        "channel": "generic",
        "pin_time_to_live": 5,
        "pin_length": 4,
        "message_type": "NUMERIC"
    }
    
    print(f"Sending to Termii: {phone}") # Don ganin logs a Render
    r = requests.post(url, json=payload)
    
    print(f"TERMII SAYS: {r.text}") # Wannan zai nuna mana ainihin kuskuren
    return jsonify(r.json())

@app.route("/")
def home():
    return "Zango Backend is Running"

if __name__ == "__main__":
    app.run(debug=True)
