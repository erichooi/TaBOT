from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from prompt_toolkit import prompt
from wit import Wit
from dateutil import parser

import event
import config

access_token = config.get_yml_section("wit")["access_token"]
client = Wit(access_token=access_token)

class TaBOTError(Exception):
    """ Basic exception for errors raised by TaBOT """
    def __init__(self, msg = None):
        if msg is None:
            msg = "An error occurred"
        super(Exception, self).__init__(msg)

class NotEntityFound(TaBOTError):
    """ When not entity found """
    def __init__(self):
        msg = "Not entity found"
        super(TaBOTError, self).__init__(msg)

class TaBOT:
    def __init__(self):
        self._resp = dict()
        self.entity_answer = {
            "event_only": ["event"],
            "event_with_date": ["event", "dateformat"],
            "bye": ["bye", "greetings"],
            "greetings": ["greetings"]
        }
        self._entities = dict() # get the entities from user question
        self._date = dict() # get the date from user question if the question has date input
        self._answer_entity_bank = [] # get the possible combination of entity to answer user question
        self._answer_type = "" # get the type of answer in self.entity_answer

    def _send_message(self, message):
        self._resp = client.message(message)

    def _update_entities(self):
        """
        :param dict resp: response message from wit ai after sending message
        :return int ErrorCode: refer ErrorCode class
        """
        print(self._entities)
        self._entities = self._resp["entities"]
        if not self._entities:
            raise NotEntityFound
        else:
            pass

    def _extract_and_format_date(self):
        """
        :return void: update the self._data
        """
        date_value = self._entities["dateformat"][0]["value"]
        date = parser.parse(date_value)
        self._date["day"] = date.day
        self._date["month"] = date.month
        self._date["year"] = date.year

    def _update_answer_type(self):
        """
        :return void: update the self._answer_type
        """
        # update the answer entity bank
        for entity in self._entities:
            if entity == "dateformat":
                self._extract_and_format_date()
            self._answer_entity_bank.append(entity)
        # get the answer type
        for key, value in self.entity_answer.items():
            if sorted(value) == sorted(self._answer_entity_bank):
                self._answer_type = key

    def get_answer_type(self):
        """
        :return string self._answer_type:
        """
        return self._answer_type

    def generate_answer_type(self, message):
        """
        Process to get the answer type
        :param string message: Question that asked by user
        :return void: run the process of getting the answer_type
        """
        self._send_message(message)
        try:
            self._update_entities()
            self._update_answer_type()
        except NotEntityFound as e:
            print(e)

    def get_date(self):
        """
        :return dict self._date: the date of from the question of user
        """
        return self._date

    # /// this part code only for terminal printing and testing
    # handle the asking event question
#     def answer_event(self):
#         event.print_event_info()
#
# def main():
#     print("Hi, I am TaBOT :)")
#     while True:
#         chatbot = TaBOT()
#         message = prompt(">>> ").rstrip()
#         chatbot.generate_answer_type(message)
#         answer_type = chatbot.get_answer_type()
#
#         if answer_type == "event_only":
#             print(event.get_event_info().encode("utf8"))
#         elif answer_type == "greetings":
#             print("Hi, I am a chatbot that can help you to understand more about UTM Malaysia.")
#             print("Feel free to ask me any question about UTM Malaysia.")
#         elif answer_type == "bye":
#             print("Nice to talk to you.")
#             print("Bye bye.....")
#             break
#         elif answer_type == "event_with_date":
#             date = chatbot.get_date()
#             day = date["day"]
#             month = date["month"]
#             year = date["year"]
#             print(date["day"])
#             print(date["month"])
#             print(date["year"])
#             print(event.get_event_info_date(day, month, year).encode("utf8"))
#         else:
#             print("Sorry, I still cannot answer that question now. But in the near future, I will be able to do so!!! :)")
#             print("For now, you can ask question like this:")
#             print("    What is the event in UTM?")
#             print("    Is there any event in Aug 2017?")
#
# if __name__ == "__main__":
#     main()
