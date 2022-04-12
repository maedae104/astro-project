import requests
from bs4 import BeautifulSoup

URL = "https://mooncalendar.astro-seek.com/"
page = requests.get(URL)

print(page.text)

soup = BeautifulSoup(page.content, "html.parser")



# results = soup.find(name="Date")
# dates = results.find_all("div", class_="card-content")
