import requests, json
from bs4 import BeautifulSoup
from flask import jsonify

URL = "https://mooncalendar.astro-seek.com/"
page = requests.get(URL)


soup = BeautifulSoup(page.content, "html.parser")

table = soup.find(id="tabs_content_container")
rows = table.find_all("tr", class_="ruka")
moon_dict = { }



for row in rows:
    moon_dt = row.text.strip('\n')
    moon_tokens = moon_dt.strip('\n').split(' ')
    moon_phase = ''
    moon_ph_keys = []
    day_and_date = moon_tokens[0] + moon_tokens[1]
    new_date = day_and_date.strip()
    new_date = new_date.replace("\n", " ")
    new_date = new_date.split(" ")
    date_only = new_date[2]
    
    
    if 'Crescent' in moon_tokens[3]:
        moon_phase = moon_tokens[2] + ' ' + moon_tokens[3]
        
        if "Waxing Crescent" in moon_phase:
            moon_ph_keys.append("Waxing Crescent")
        elif "Waning Crescent" in moon_phase:
            moon_ph_keys.append("Waning Crescent")

    if 'Gibbous' in moon_tokens[3]:
        moon_phase = moon_tokens[2] + ' ' + moon_tokens[3]
        
        if "Waxing Gibbous" in moon_phase:
            moon_ph_keys.append("Waxing Gibbous")
        elif "Waning Gibbous" in moon_phase:
            moon_ph_keys.append("Waning Gibbous")

    if 'Quarter' in moon_tokens[2]:
        moon_phase = moon_tokens[1] + ' ' + moon_tokens[2]    
        
        if "First Quarter" in moon_phase:
            moon_ph_keys.append("First Quarter")
        elif "Last Quarter" in moon_phase:
            moon_ph_keys.append("Last Quarter")
    
    if 'FULL' in moon_tokens[1]:
        moon_phase = moon_tokens[1] + ' ' + moon_tokens[2] 

        if "FULL MOON" in moon_phase:
            moon_ph_keys.append("Full Moon")
        
    
    if 'NEW' in moon_tokens[1]:
        moon_phase = moon_tokens[1] + ' ' + moon_tokens[2] 

        if "NEW MOON" in moon_phase:
            moon_ph_keys.append("New Moon")


    moon_dict[date_only] = moon_ph_keys









