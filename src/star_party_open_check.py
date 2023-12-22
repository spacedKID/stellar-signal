import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def check_observatory_status(url):
    # Send a GET request to the observatory's website
    response = requests.get(url)
    response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the observatory status - Adjust the selector as needed
    status_element = soup.find_all(string=lambda text: "OBSERVATORY STATUS" in text)
    
    if status_element:
        # Assuming the status is in a parent element of the found string
        status_text = ' '.join([str(elem.parent.get_text(strip=True)) for elem in status_element])
        return status_text
    else:
        return "Observatory status not found."


def get_stargazing_forecast(api_key, latitude, longitude):
    url = f"https://api.stormglass.io/v2/astronomy/point?lat={latitude}&lng={longitude}"

    headers = {
        'Authorization': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def get_stargazing_forecast(api_key, latitude, longitude):
    url = f"https://api.stormglass.io/v2/astronomy/point?lat={latitude}&lng={longitude}"

    headers = {
        'Authorization': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def find_next_wednesday():
    today = datetime.utcnow().date()
    days_until_wednesday = (2 - today.weekday() + 7) % 7  # 2 represents Wednesday
    if days_until_wednesday == 0:
        days_until_wednesday = 7
    next_wednesday = today + timedelta(days=days_until_wednesday)
    return next_wednesday

def summarize_forecast(forecast_data):
    next_wednesday = find_next_wednesday()

    for day_data in forecast_data['data']:
        forecast_date = datetime.fromisoformat(day_data['time']).date()
        if forecast_date == next_wednesday:
            moon_phase = day_data['moonPhase']['current']['text']
            moonrise = day_data['moonrise']
            moonset = day_data['moonset']
            astronomical_dawn = day_data['astronomicalDawn']
            astronomical_dusk = day_data['astronomicalDusk']
            
            summary = (
                f"Stargazing Forecast for {next_wednesday}:\n"
                f"- Moon Phase: {moon_phase}\n"
                f"- Moonrise: {moonrise}\n"
                f"- Moonset: {moonset}\n"
                f"- Astronomical Dawn: {astronomical_dawn}\n"
                f"- Astronomical Dusk: {astronomical_dusk}\n"
            )
            return summary

    return "No data available for the upcoming Wednesday."

