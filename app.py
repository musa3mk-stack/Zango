from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app) 

# Wannan zai karba daga Render Environment
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
    
    # Payload din da Termii yake bukata
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
    
    # Headers da ake bukata don tabbatar da cewa JSON ne
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Sending to Termii: {phone}") 
    
    try:
        # Aika request tare da headers
        r = requests.post(url, json=payload, headers=headers)
        print(f"TERMII SAYS: {r.text}")
        return jsonify(r.json())
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Zango Backend is Running"

if __name__ == "__main__":
    app.run(debug=True)
