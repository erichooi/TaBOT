import requests
import re
from bs4 import BeautifulSoup

session = requests.Session()
headers = {
    "Referer": "https://www.google.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
}
session.headers.update(headers)

def get_webpage_content(url):
    """
    :param string url: URL for the event page that need to scrape
    :return string content: HTML page
    """
    content = session.get(url, verify=False).text
    return content

def get_event_data(event_content, list_type="li"):
    """
    :param string event_content: HTML page for searching
    :param string list_type: tag of list that need to search ("li" for events main page, "div" for event with date)
    :return list event_list: contain the dictionary of information about the event
    """
    soup = BeautifulSoup(event_content, "html.parser")
    event = soup.find("ul", {"class": "category_list_view"})
    try:
        data = event.li.ul
    except AttributeError:
        data = event
    timing_pattern = re.compile(r"Start Date:\s+(?P<startDate>.*?)[\n]*End Date:\s+(?P<endDate>.*?)[\t\n]Time:[\s\t\n]+(?P<time>.*?)\n")
    location_pattern = re.compile(r"Location\s:[\s\n]+(?P<location>.*?)\n")
    event_list = []
    for info in data.find_all(list_type):
        timing = timing_pattern.search(info.select("p")[0].text + "\n")
        location = location_pattern.search(info.select("p")[1].text + "\n")
        event_list.append(
            {
                "title": info.h3.a.text,
                "url": info.a["href"],
                "imgSrc": info.a.img["src"],
                "startDate": timing.group("startDate"),
                "endDate": timing.group("endDate"),
                "time": timing.group("time"),
                "location": location.group("location")
            }
        )
    return event_list
