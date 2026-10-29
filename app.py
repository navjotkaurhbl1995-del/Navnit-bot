from flask import Flask, request
import requests, os
app = Flask(__name__)
TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_ID = os.environ.get("PHONE_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
def send_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
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
            if text in ["hi","hello","hlo"]:
                reply = "Sat Sri Akal Ji! 🙏 Welcome to Navnit Fitcoach\n3 Coaches - Diet, Workout, Lifestyle\nRoz Live: 5:00 AM & 5:20 PM\nGoal? 1-Weight Loss 2-Weight Gain 3-Skin Glow"
            else:
                reply = "Age/Weight/Height bhejdo ji, Team help karegi. Call 7347455110"
            send_message(from_num, reply)
    except: pass
    return "OK", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
