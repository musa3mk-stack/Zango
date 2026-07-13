@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    data = request.json
    phone = data.get("phone") # Backend ya karbi phone kawai
    
    if phone.startswith("0"):
        phone = "234" + phone[1:]
    
    url = "https://api.ng.termii.com/api/sms/otp/send"
    payload = {
        "api_key": TERMII_KEY, # Backend ne ya saka key din nan
        "to": phone,
        "from": "Zango",
        "sms": "Your Zango code is < 1234 >",
        "channel": "generic",
        "pin_time_to_live": 5,
        "pin_length": 4,
        "message_type": "NUMERIC"
    }
    r = requests.post(url, json=payload)
    return jsonify(r.json())
