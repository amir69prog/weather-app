from source import (
		QApplication,
		QWidget,
		loadUi,
		QIcon,
		sys,
		IconStateWeatherAPI,
		CityWeatherAPI,
		Qt,
		CityNotFoundError,
		QPixmap,
		os,
	)


os.chdir('E:/All-Project/windows/weather-app/app/main_app')


# todo : get the date and time as well
# todo : get the current location and the weather
# todo : create message box
# todo : set none fieds

class BackgroundPixmap(QPixmap):
	""" back ground image """

	def __init__(self,path):
		super().__init__(path)


class WeatherData:
	""" The class that set the information in the main """

	def __init__(self,parent,data,icon):
		self.parent = parent
		self.icon = icon
		self.data = data

	def set_icon_weather(self):
		""" set the status of weather with icon """
		if self.icon:
			self.parent.weather_state.setText(self.data['state'])
			# pixmap icon
			icon = QIcon('../images/icons/{}.png'.format(self.data['icon_state']))
			self.parent.weather_state.setIcon(icon)


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
					# the icon of weather state
					print(filtered_data)
					icon_state = IconStateWeatherAPI(filtered_data['icon_state'])()
					data_weather = WeatherData(self,filtered_data,icon_state)
					data_weather.settings()

			except CityNotFoundError:
				# todo : create message box ,set none fileds
				pass
		else:
			# todo : create message box ,set none fileds
			pass


# run app
if __name__ == '__main__':
	app = QApplication(sys.argv)

	main_weather = MainWeather()
	main_weather.show()

	app.exec_()