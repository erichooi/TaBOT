from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from enum import Enum
from prompt_toolkit import prompt
from wit import Wit

import event
import config

access_token = config.get_yml_section("wit")["access_token"]
client = Wit(access_token=access_token)

class ErrorCode(Enum):
    UNDERSTAND = 0
    NOT_ENTITIES_FOUND = 1
    NOT_UNDERSTAND = 2
    START_CONVERSATION = 3
    CONTINUE_CONVERSATION = 4
    END_CONVERSATION = 5

class TaBOT:
    def __init__(self):
        self.entity_answer = {
            "event_only": ["event"],
            "event_with_date": ["event", "dateformat"],
            "bye": ["bye", "greetings"],
            "greetings": ["greetings"]
        }
        self.entities = dict() # get the entities from user question
        self.date = dict() # get the date from user question if the question has date input
        self.answer_entity_bank = [] # get the possible combination of entity to answer user question

    def send_message(self, message):
        resp = client.message(message)
        return resp

    def update_entities(self, resp):
        self.entities = resp["entities"]
        if not self.entities:
            return ErrorCode.NOT_ENTITIES_FOUND
        else:
            return None

    # handle the asking event question
    def answer_event(self):
        event.print_event_info()

    def extract_and_format_date(self):
        day = 1
        month = 1
        year = 1
        try:
            day = self.entities['dateformat'][0]['entities']['day'][0]['value']
            month = self.entities['dateformat'][0]['entities']['month'][0]['value']
            year = self.entities['dateformat'][0]['entities']['year'][0]['value']
        except KeyError as e:
            pass
        self.date["day"] = day
        self.date["month"] = month
        self.date["year"] = year

    def return_message(self):
        answer_type = ""
        # update the answer entity bank
        for entity in self.entities:
            if entity == "dateformat":
                self.extract_and_format_date()
            self.answer_entity_bank.append(entity)
        # get the answer key / answer type
        for key, value in self.entity_answer.items():
            if sorted(value) == sorted(self.answer_entity_bank):
                answer_type = key
        # answer based on different answer_type
        if answer_type == "event_only":
            event.print_event_info()
            return ErrorCode.CONTINUE_CONVERSATION
        elif answer_type == "greetings":
            print("Hi, I am a chatbot that can help you to understand more about UTM Malaysia.")
            print("Feel free to ask me any question about UTM Malaysia.")
            return ErrorCode.CONTINUE_CONVERSATION
        elif answer_type == "bye":
            print("Nice to talk to you.")
            print("Bye bye.....")
            return ErrorCode.END_CONVERSATION
        elif answer_type == "event_with_date":
            event.print_event_info_date(self.date["day"], self.date["month"], self.date["year"])
        else:
            print("Sorry, I still cannot answer that question now. But in the near future, I will be able to do so!!! :)")
            print("For now, you can ask question like this:")
            print("    What is the event in UTM?")
            print("    Is there any event in Aug 2017?")
            return ErrorCode.CONTINUE_CONVERSATION

def main():
    print("Hi, I am TaBOT :)")
    while True:
        try:
            chatbot = TaBOT()
            message = prompt(">>> ").rstrip()
            print()
            resp = chatbot.send_message(message)
            chatbot.update_entities(resp)
            message_code = chatbot.return_message()
            print()
            if message_code == ErrorCode.END_CONVERSATION:
                break
        except(KeyboardInterrupt, EOFError):
            return

if __name__ == "__main__":
    main()
