import requests
import os
from dotenv import load_dotenv

class Weather():
    def __init(self):
        load_dotenv()
        self.key = os.getenv('WEATHER_API_KEY')
        
    def get_weather(self, city):
        response = "El clima en la ciudad " + city + "se presenta como caluroso y nublado"
        return response
