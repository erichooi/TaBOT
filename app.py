from flask import Flask, request
from pymessenger import Bot
from tabot import TaBOT

import config
import event

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

        if ("message" in message_content.keys()):
            print(message_content["message"]["text"])
        else:
            print("no message")
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

    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True, port=80)