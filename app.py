from flask import Flask, request
import requests, os
app = Flask(__name__)

TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_ID = os.environ.get("PHONE_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

@app.route("/")
def home():
    return "Navnit Fitcoach Bot is LIVE! ✅ Your auto reply bot is working!"

def send_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"messaging_product": "whatsapp", "to": to, "text": {"body": text}}
    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        msg_data = data['entry'][0]['changes'][0]['value']
        if 'messages' in msg_data:
            from_num = msg_data['messages'][0]['from']
            text = msg_data['messages'][0]['text']['body'].lower()
            
            # Navnit Fitcoach Auto Reply
            if "hi" in text or "hello" in text:
                reply = "Hi ji! Main Navnit Fitcoach Bot haan! 💪 Diet plan chahida? Weight loss? Dasso ki madad kar sakda haan?"
            elif "diet" in text or "plan" in text:
                reply = "Diet plan layi tuhada weight, height dasso ji, mai plan bhej dunga! 🥗"
            elif "fees" in text or "price" in text:
                reply = "Fees details layi Navnit naal gal karo ji - 100% result! 🔥"
            else:
                reply = "Satsriakal ji! Navnit Fitcoach to contact karna chahte ho? 'HI' likho!"
            
            send_message(from_num, reply)
    except:
        pass
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
