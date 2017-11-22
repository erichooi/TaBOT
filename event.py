import random
import config
import scraper

EVENT_URL = config.get_yml_section("url")["event_url"]

# deprecated, replace with the list view
def get_event_info():
    """
    :return string event_info: get the information for the upcoming event
    """
    event_page = scraper.get_webpage_content(EVENT_URL)
    event_data = scraper.get_event_data(event_page, "li")
    event_data = event_data[0:2]
    event_info = ""
    for data in event_data:
        event_info += data["title"] + "\n"
        event_info += "Start Date: " + data["startDate"] + "\n"
        event_info += "End Date: " + data["endDate"] + "\n"
        event_info += "Time: " + data["time"] + "\n"
        event_info += "Location: " + data["location"] + "\n"
    return event_info

# deprecated, replace with the list view
def get_event_info_date(day, month, year):
    """
    :param int day: day that need to search
    :param int month: month that need to search
    :param int year: year that need to search
    :return string event_info: information of the upcoming event
    """
    event_page = scraper.get_webpage_content(EVENT_URL + "/?s=Calender-Event&m=" + str(year) + str(month) + str(day))
    event_data = scraper.get_event_data(event_page, "div")
    event_data = event_data[0:2]
    event_info = ""
    for data in event_data:
        event_info += data["title"] + "\n"
        event_info += "Start Date: " + data["startDate"] + "\n"
        event_info += "End Date: " + data["endDate"] + "\n"
        event_info += "Time: " + data["time"] + "\n"
        event_info += "Location: " + data["location"] + "\n"
    return event_info

def get_event_info_list_view():
    """
    :return json payload: payload for the request of list template for facebook
    """
    event_page = scraper.get_webpage_content(EVENT_URL)
    event_data = scraper.get_event_data(event_page, "li")
    three_random_number = random.sample(range(0, len(event_data)), 3)
    random_event_data = [event_data[x] for x in three_random_number]
    elements_list = []
    for data in random_event_data:
        element = {
            "title": data["title"],
            "image_url": data["imgSrc"],
            "buttons": [
                {
                    "title": "View",
                    "url": data["url"],
                    "type": "web_url",
                    "webview_height_ratio": "compact"
                }
            ]
        }
        elements_list.append(element)
    payload = {
        "template_type": "list",
        "top_element_style": "compact",
        "elements": elements_list,
        "buttons": [
            {
                "title": "View More",
                "type": "web_url",
                "url": EVENT_URL
            }
        ]
    }

    return payload

def get_event_info_date_list_view(day, month, year):
    """
    :param int day: day that need to search
    :param int month: month that need to search
    :param int year: year that need to search
    :return json payload: payload for the request of list template for facebook
    """
    event_page = scraper.get_webpage_content(EVENT_URL + "/?s=Calender-Event&m=" + str(year) + str(month) + str(day))
    event_data = scraper.get_event_data(event_page, "div")
    if len(event_data) != 0:
        if len(event_data) < 2:
            data = event_data[0]
            payload = {
                "template_type": "generic",
                "elements": [
                    {
                        "title": data["title"],
                        "image_url": data["imgSrc"],
                        "default_action": {
                            "type": "web_url",
                            "url": data["url"],
                            "webview_height_ratio": "tall"
                        },
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": data["url"],
                                "title": "View Website"
                            }
                        ]
                    }
                ]
            }
        else:
            event_data = event_data[0:2]
            elements_list = []

            for data in event_data:
                element = {
                    "title": data["title"],
                    "image_url": data["imgSrc"],
                    "buttons": [
                        {
                            "title": "View",
                            "url": data["url"],
                            "type": "web_url",
                            "webview_height_ratio": "compact"
                        }
                    ]
                }
                elements_list.append(element)

            payload = {
                "template_type": "list",
                "top_element_style": "compact",
                "elements": elements_list,
                "buttons": [
                    {
                        "title": "View More",
                        "type": "web_url",
                        "url": EVENT_URL + "/?s=Calender-Event&m=" + str(year) + str(month) + str(day)
                    }
                ]
            }
    else:
        payload = {}

    return payload
