from flask import Flask, request
from tabot import TaBOT

import config
import event
import requests
import json

facebook_access_token = config.get_yml_section("facebook")["access_token"]

app = Flask(__name__)

fail_text = "Sorry, I cannot help you with that.\n"
fail_text += "Type 'help' to know more about what I can do"

help_text = "You can ask something similar like this:\n"
help_text += "1. Is there any event that is happening today?\n"
help_text += "2. Find me some event on 27/11/2017.\n" # search event by date
help_text += "3. Any event near UTM KL." # search event by location

greeting_text = "Hello! I am TaBot. You can ask me about event information in UTM"

bye_text = "Bye..."

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

        #TODO the attachments is for any sticker
        if ("message" in message_content.keys() and "is_echo" not in message_content["message"].keys() and "attachments" not in message_content["message"].keys()):
            print(message_content)
            message = message_content["message"]["text"]
            if message.lower() == "help":
                send_text_message(facebook_access_token, sender_id, help_text)
            else:
                tabot.generate_answer_type(message)
                answer_type = tabot.get_answer_type()
                # TODO testing purpose
                print(answer_type)
                
                if answer_type == "event_only":
                    send_list_view(facebook_access_token, sender_id, event.get_event_info_list_view())
                elif answer_type == "event_with_date":
                    date = tabot.get_date()
                    day = date["day"]
                    month = date["month"]
                    year = date["year"]
                    send_list_view(facebook_access_token, sender_id, event.get_event_info_date_list_view(day, month, year))
                elif answer_type == "event_with_location":
                    location = tabot.get_location()
                    #TODO test
                    print(location)
                    send_list_view(facebook_access_token, sender_id, event.get_event_info_location_list_view(location))
                elif answer_type == "greetings":
                    send_text_message(facebook_access_token, sender_id, greeting_text)
                elif answer_type == "bye":
                    send_text_message(facebook_access_token, sender_id, bye_text)
                else:
                    send_text_message(facebook_access_token, sender_id, fail_text)
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

def send_list_view(token, recipient_id, payload):
    """
    :param string token: access token for facebook messenger
    :param string recipient_id: id of the recipient
    :param json payload: the payload that need to send
    :return void: send the list view message through facebook messenger
    """
    if bool(payload) == False:
        send_text_message(token, recipient_id, "Sorry there is no event on this date!!")
    else:
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

if __name__ == "__main__":
    app.run(debug=True, port=80)