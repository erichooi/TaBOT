from flask import Flask, request
from tabot import TaBOT

import config
import event
import requests
import json

facebook_access_token = config.get_yml_section("facebook")["access_token"]

app = Flask(__name__)

help_text = "You can ask me the following question.\n"
help_text += "1. Any event in UTM lately?\n"
help_text += "2. Any event on 11/11/2017?"

greeting_text = "Hi! I am TaBot."

@app.route("/webhook", methods=["GET"])
def verity():
    # webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Verify success", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    tabot = TaBOT()
    data = request.get_json()
    if data["object"] == "page":
        entry = data["entry"]
        message_content = entry[0]["messaging"][0]
        sender_id = message_content["sender"]["id"]

        if ("message" in message_content.keys() and "is_echo" not in message_content["message"].keys()):
            print(message_content)
            message = message_content["message"]["text"]
            tabot.generate_answer_type(message)
            answer_type = tabot.get_answer_type()
            if answer_type == "event_only":
                # send_text_message(facebook_access_token, sender_id, event.get_event_info())
                send_list_view(facebook_access_token, sender_id, event.get_event_info_list_view())
            elif answer_type == "event_with_date":
                date = tabot.get_date()
                day = date["day"]
                month = date["month"]
                year = date["year"]
                # send_text_message(facebook_access_token, sender_id, event.get_event_info_date(day, month, year))
                send_list_view(facebook_access_token, sender_id, event.get_event_info_date_list_view(day, month, year))
            elif answer_type == "greetings":
                send_text_message(facebook_access_token, sender_id, greeting_text)
            elif answer_type == "bye":
                send_text_message(facebook_access_token, sender_id, "Bye...")
            else:
                send_text_message(facebook_access_token, sender_id, help_text)
        else:
            pass
    else:
        pass

    return "ok", 200

def send_text_message(token, recipient_id, text):
    """
    :param string token: the facebook token
    :param string recipient_id: id of the recipient
    :param string text: the text need to send
    :return void: send the message through facebook messenger
    """
    req = requests.post("https://graph.facebook.com/v2.6/me/messages",
                        params = {"access_token": token},
                        data = json.dumps({
                            "recipient": {"id": recipient_id},
                            "message": {"text": text}
                        }),
                        headers = {"Content-type": "application/json"})
    if req.status_code != requests.codes.ok:
        print(req.text)

def send_list_view(token, recipient_id, payload):
    """
    :param string token: access token for facebook messenger
    :param string recipient_id: id of the recipient
    :param json payload: the payload that need to send
    :return void: send the list view message through facebook messenger
    """
    req = requests.post("https://graph.facebook.com/v2.6/me/messages",
                        params = {"access_token": token},
                        data = json.dumps({
                            "recipient": {"id": recipient_id},
                            "message": {
                                "attachment": {
                                    "type": "template",
                                    "payload": payload
                                }
                            }
                        }),
                        headers = {"Content-type": "application/json"})
    if req.status_code != requests.codes.ok:
        print(req.text)

if __name__ == "__main__":
    app.run(debug=True, port=80)