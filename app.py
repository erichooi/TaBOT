from flask import Flask, request
from pymessenger import Bot
from tabot import TaBOT

import config
import event
import requests
import json

facebook_access_token = config.get_yml_section("facebook")["access_token"]
facebook_bot = Bot(facebook_access_token)
tabot = TaBOT()

app = Flask(__name__)

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
    data = request.get_json()
    if data["object"] == "page":
        entry = data["entry"]
        message_content = entry[0]["messaging"][0]
        sender_id = message_content["sender"]["id"]
        recipient_id = message_content["recipient"]["id"]

        if ("message" in message_content.keys() and "is_echo" not in message_content["message"].keys()):
            print(message_content)
            message = message_content["message"]["text"]
            tabot.generate_answer_type(message)
            answer_type = tabot.get_answer_type()
            if answer_type == "event_only":
                send_message(facebook_access_token, sender_id, event.get_event_info())
            elif answer_type == "greetings":
                send_message(facebook_access_token, sender_id, "Hi! anything I can help?\nFeel free to talk to me")
            elif answer_type == "bye":
                send_message(facebook_access_token, sender_id, "Bye...")
        else:
            pass

    return "ok", 200

def send_message(token, recipient_id, text):
    """
    :param token:
    :param recipient_id:
    :param text:
    :return:
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

        # if ("message" in message_content.keys()):
        #     if ("text" in message_content["message"].keys()):
        #         print(message_content["message"]["text"])
        #         # send text to wit ai to process
        #         tabot.generate_answer_type(message_content["message"]["text"])
        #         answer_type = tabot.get_answer_type()
        #         if answer_type == "event_only":
        #             facebook_bot.send_text_message(sender_id, "event only")
        #             # facebook_bot.send_text_message(sender_id, event.get_event_info())
        #         elif answer_type == "greetings":
        #             facebook_bot.send_text_message(sender_id, "Hi! anything I can help?\nFeel free to talk to me")
        #     else:
        #         facebook_bot.send_text_message(sender_id, "no text found in message")
        # else:
        #     facebook_bot.send_text_message(sender_id, "no message sent")


if __name__ == "__main__":
    app.run(debug=True, port=80)