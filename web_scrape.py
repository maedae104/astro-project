import requests, json
from bs4 import BeautifulSoup
from flask import jsonify

moon_URL = "https://mooncalendar.astro-seek.com/moon-phases-calendar-may-2022"
moon_page = requests.get(moon_URL)

retro_URL = "https://horoscopes.astro-seek.com/mercury-retrograde-shadow-retroshade-periods"
retro_page = requests.get(retro_URL)

retro_soup = BeautifulSoup(retro_page.content, "html.parser")
moon_soup = BeautifulSoup(moon_page.content, "html.parser")

table = moon_soup.find(id="tabs_content_container")
moon_rows = table.find_all("tr", class_="ruka")
moon_dict = { }


retro_table = retro_soup.find("table")
retro_rows = retro_table.find_all("tr")

for r_row in retro_rows:
    retro_dt = r_row.text.strip('\n')
    retro_dt = retro_dt.replace("\n", " ")
    retro_tokens = retro_dt.strip('\n').split(' ')
    retro_tokens =  list(filter(None, retro_tokens))
    retro_phase = ''
    retro_ph_keys = []
    retro_dates = []
    retro_dict = {}
    
    if retro_tokens == []:
        pass
    else:
        r_month_date = retro_tokens[0] + retro_tokens[1]
        retro_dates.append(r_month_date)
    
        if "Retrograde" in retro_tokens[4] and "Begins" in retro_tokens[5]:
            retro_phase = "Pre-Shadow Ends and Retrograde Begins"

        elif "Retrograde" in retro_tokens[4] and "Ends" in retro_tokens[5]:
            retro_phase = "Retrograde Ends and Post-Shadow Begins"

        elif "Post-Shadow" in retro_tokens[4] and "Ends" in retro_tokens[5]:
            retro_phase = "Post-Shadow Ends"

        elif "Pre-Shadow" in retro_tokens[4] and "Begins" in retro_tokens[5]:
            retro_phase = "Pre-shadow Begins"


    for date in retro_dates:
        retro_dict[date] = retro_phase
    
        print(retro_dict)

for row in moon_rows:
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









