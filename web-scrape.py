import requests, json
from bs4 import BeautifulSoup

URL = "https://mooncalendar.astro-seek.com/"
page = requests.get(URL)

# print(page.text)

soup = BeautifulSoup(page.content, "html.parser")

table = soup.find(id="tabs_content_container")
dates = table.find_all("div", class_="tab_content")

for table_element in dates:
    print(table_element)