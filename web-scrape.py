import requests, json
from bs4 import BeautifulSoup

URL = "https://mooncalendar.astro-seek.com/"
page = requests.get(URL)


soup = BeautifulSoup(page.content, "html.parser")

table = soup.find(id="tabs_content_container")
rows = table.find_all("tr", class_="ruka")

for row in rows:
    print(row.prettify())

