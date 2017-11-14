import config
import scraper

EVENT_URL = config.get_yml_section("url")["event_url"]

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

# TODO test only
def get_event_info_list_view():
    """
    :return string event_info: get the information for the upcoming event
    """
    event_page = scraper.get_webpage_content(EVENT_URL)
    event_data = scraper.get_event_data(event_page, "li")
    event_data = event_data[0:2]
    event_info = ""
    # for data in event_data:
    #     event_info += data["title"] + "\n"
    #     event_info += "Start Date: " + data["startDate"] + "\n"
    #     event_info += "End Date: " + data["endDate"] + "\n"
    #     event_info += "Time: " + data["time"] + "\n"
    #     event_info += "Location: " + data["location"] + "\n"
    payload = {
        "template_type": "list",
        "top_element_style": "compact",
        "elements": [
            {
                "title": "Title",
                "image_url": "https://www.facebook.com/images/fb_icon_325x325.png",
                "buttons": [
                    {
                        "title": "View",
                        "type": "web_url",
                        "webview_height_ratio": "tall",
                        "fallback_url": "https://test.com"
                    }
                ]
            },
            {
                "title": "fun to test",
                "subtitle": "very fun"
            }
        ],
        "buttons": [
            {
                "title": "View More",
                "type": "postback",
                "payload": "payload"
            }
        ]
    }
    return payload