import config
import scraper

EVENT_URL = config.get_yml_section("url")["event_url"]

def print_event_info():
    """
    :return void: print the information for the upcoming event
    """
    event_page = scraper.get_webpage_content(EVENT_URL)
    event_data = scraper.get_event_data(event_page, "li")
    for data in event_data:
        try:
            print(data["title"])
        except UnicodeEncodeError:
            print(data["title"].replace("\u2019", "'"))
        print("Start Date: " + data["startDate"])
        print("End Date: " + data["endDate"])
        print("Time: " + data["time"])
        print("Location: " + data["location"])
        print()

def print_event_info_date(day, month, year):
    """
    :param int day: day that need to search
    :param int month: month that need to search
    :param int year: year that need to search
    :return void: print the information for the event based on the date
    """
    event_page = scraper.get_webpage_content(EVENT_URL + "/?s=Calender-Event&m=" + str(year) + str(month) + str(day))
    event_data = scraper.get_event_data(event_page, "div")
    for data in event_data:
        try:
            print(data["title"])
        except UnicodeEncodeError:
            print(data["title"].replace("\u2019", "'"))
        print("Start Date: " + data["startDate"])
        print("End Date: " + data["endDate"])
        print("Time: " + data["time"])
        print("Location: " + data["location"])
        print()
