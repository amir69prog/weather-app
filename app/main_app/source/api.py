import requests
import os
from .exceptions import CityNotFoundError



class WeatherAPI:
	""" The API of open weather map """
	
	def get_api_key(self):
		API_KEY_FILE = open('../weather_api_key.txt','r')
		with API_KEY_FILE as file:
			api_key = file.read()
			file.close()
		self.api_key = api_key


	def __init__(self,url):
		self.url = url
		self.get_api_key()


class IconStateWeatherAPI(WeatherAPI):
	""" get the Icon weather state """
	
	def __init__(self,icon):
		super().__init__('http://openweathermap.org/img/wn/10d@2x.png')
		self.icon = icon
		self.url_icon = "http://openweathermap.org/img/wn/{icon_code}@2x.png".format(icon_code=self.icon)
	
	def __call__(self):
		request = requests.get(self.url_icon)
		response = request.content
		return response


class CityWeatherAPI(WeatherAPI):
	""" the api that it's get the weather of cities """

	def __init__(self):
		super().__init__('http://api.openweathermap.org/data/2.5/weather')

	def get_weather(self,city_name):
		""" Get the weather json data """
		response = None
		print(city_name)
		if city_name:
			parameters = {
				'q':city_name,
				'APPID':self.api_key,
				'units':'metric',
			}
			request = requests.get(self.url,params=parameters)
			response = request.json()
			if response.get('cod') and response.get('cod') == '404':
				msg = 'Sorry i could\'nt found the %r' % city_name
				raise CityNotFoundError(msg)
		return response

	@staticmethod
	def filter_weather_data(data: dict) -> dict:
		""" Filter the weather data """
		try:
			final_data = {
				'state':data['weather'][0]['main'],
				'icon_state':data['weather'][0]['icon'],
				'temp':data['main']['temp'],
				'humidity':data['main']['humidity'],
				'wind_speed':data['wind']['speed'],
				'city_name':data['name'],
				'country':data['sys']['country'],
				'timezone':data['timezone'],
			}
		except KeyError as error:
			final_data = data

		return final_data
