from source import (
	QApplication,
	QWidget,
	loadUi,
	QIcon,
	QPixmap,
	Qt,
	sys,
	os,
	# api
	IconStateWeatherAPI,
	CityWeatherAPI,
	# execptions
	CityNotFoundError,
	InvalidAPIKeyError,
	APIFileNotFoundError,
	# messages
	APIFileNotFoundMessage,
	CityNotFoundMessage,
	InvalidAPIKeyMessage,
	ConnectionErrorMessage,
)
from requests.exceptions import ConnectionError
from timezonefinder import TimezoneFinder
import pytz,datetime


os.chdir('E:/All-Project/windows/weather-app/app/main_app')



class TimezoneLocation:
	@staticmethod
	def get_timezone(latitude,longitude):
		tz_finder = TimezoneFinder()
		return tz_finder.timezone_at(lng=longitude, lat=latitude)

class TimeRegion:
	def get_time(self,timezone):
		return datetime.datetime.now(pytz.timezone(timezone))


class BackgroundPixmap(QPixmap):
	""" back ground image """

	def __init__(self,path):
		super().__init__(path)


class WeatherData:
	""" The class that set the information in the main """

	def __init__(self,parent,data,icon,time):
		self.parent = parent
		self.icon = icon
		self.data = data
		self.val_time = time

	def set_icon_weather(self):
		""" set the status of weather with icon """
		if self.icon:
			self.parent.weather_state.setText(self.data['state'])
			# pixmap icon
			icon = QIcon('../images/icons/{}.png'.format(self.data['icon_state']))
			self.parent.weather_state.setIcon(icon)

	def time_format(self):
		formatted_time = '{0:%H}:{0:%M}:{0:%S}'.format(self.val_time)
		return formatted_time

	def set_background(self):
		""" Set the background """
		try:
			pixmap_file = BackgroundPixmap(f'../images/photoes/{self.data["state"]}.jpg')
		except:
			pixmap_file = BackgroundPixmap(f'../images/photoes/blur.jpg')
		self.parent.background.setPixmap(pixmap_file)


	def settings(self):
		""" Set Data """
		template_temp = str(self.data['temp']) + '°C'
		self.parent.temp.setText(template_temp)
		self.parent.wind.setText(str(self.data['wind_speed']))
		self.parent.humidity.setText(str(self.data['humidity']) + '%')
		self.parent.time.setText('time : ' + self.time_format())
		self.set_icon_weather()
		self.set_background()



class MainWeather(QWidget):
	""" the main page of weather app """

	def __init__(self):
		super().__init__()
		loadUi('../ui/main.ui',self)
		self.settings() # set the details

		# Signals
		self.search_btn.clicked.connect(self.search_weather)

	def settings(self):
		""" Set the Detail information """
		self.setWindowTitle("Weather")
		self.setWindowIcon(QIcon('../images/icons/icon_summer.png'))
		self.setFixedSize(399,576)


	def search_weather(self):
		""" The Main Method: it's get the weather of cities """
		city_name = self.region.text()
		if city_name:
			try:
				# the city api
				weather = CityWeatherAPI()
				# take whole parameters of api
				data = weather.get_weather(city_name)
				if data:
					# filter to the standard data
					filtered_data = weather.filter_weather_data(data)
					# get the timein the city
					timezone_location = TimezoneLocation()
					timezone_ = timezone_location.get_timezone(
						filtered_data['lat'],
						filtered_data['lon']
					)
					time = TimeRegion().get_time(timezone_)
					# the icon of weather state
					icon_state = IconStateWeatherAPI(filtered_data['icon_state'])()
					data_weather = WeatherData(self,filtered_data,icon_state,time)
					data_weather.settings()

			except APIFileNotFoundError as error_desc:
				self.set_empty_fields()
				message = APIFileNotFoundMessage(self,str(error_desc))
				message.exec_()
			except InvalidAPIKeyError as error_desc:
				self.set_empty_fields()
				message = InvalidAPIKeyMessage(self,str(error_desc))
				message.exec_()
			except ConnectionError:
				self.set_empty_fields()
				text = 'Connection error\nplease check your connection...'
				message = APIFileNotFoundMessage(self,text)
				message.exec_()
			except CityNotFoundError as error_desc:
				message = CityNotFoundMessage(self,str(error_desc))
				message.exec_()


	def set_empty_fields(self):
		self.region.setText('')
		self.temp.setText('0°')
		self.humidity.setText('0%')
		self.weather_state.setText('')
		self.time.setText('')
		self.weather_state.setIcon(QIcon())
		self.background.setPixmap(QPixmap('../images/photoes/blur.jpg'))


# run app
if __name__ == '__main__':
	app = QApplication(sys.argv)

	main_weather = MainWeather()
	main_weather.show()

	app.exec_()