# my_functions.py

import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the OPENAI API key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get a response from the LLM
def get_llm_response(prompt):  # Make sure there are no typos here
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message['content'].strip()


import requests
import os


# Function to get coordinates from address using OpenCage API
def get_coordinates_from_address(address):
    API_KEY = os.getenv("OPENCAGE_API_KEY")  # Your OpenCage API Key
    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data['results']:
        geometry = data['results'][0]['geometry']
        return geometry['lat'], geometry['lng']
    else:
        return None, None


import requests
import os

#Get Openweathermap API info

import requests
import os


def get_weather(lat, lon):
    API_KEY = os.getenv("OPENWEATHER_API_KEY")  # OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    weather_data = response.json()

    # Print the full response for debugging
    print(f"API Response: {weather_data}")

    # Check if the response contains an error
    if response.status_code != 200 or 'main' not in weather_data:
        raise Exception(f"Error fetching weather data: {weather_data.get('message', 'Unknown error')}")

    # Extract useful data
    temp = weather_data['main']['temp']
    weather_description = weather_data['weather'][0]['description']

    return temp, weather_description


# Example: Call after getting lat and lon from the geocoding service
#latitude = 33.1959
#longitude = -117.3795
#temp, description = get_weather(latitude, longitude)
#print(f"Temperature: {temp}°C, Weather: {description}")

#ingredients builder
def get_user_ingredients():
    # Prompting user for available ingredients
    proteins = input("Please list the available proteins (comma-separated): ")
    vegetables = input("Please list the available vegetables (comma-separated): ")
    spices = input("Please list the available spices (comma-separated): ")

    # Store ingredients in a dictionary
    ingredients = {
        'proteins': [p.strip() for p in proteins.split(',')],  # Split by comma and remove extra spaces
        'vegetables': [v.strip() for v in vegetables.split(',')],
        'spices': [s.strip() for s in spices.split(',')]
    }

    return ingredients

def cooking_skill():
    skill_levels = ("beginner", "intermediate", "advanced")
    skill = input("Please select your cooking skill level (beginner, intermediate, advanced): ")

    while skill not in skill_levels:
        skill = input(f"Invalid input. Please select from {skill_levels}: ")

    return skill
