class CityNotFoundError(ValueError):
	""" Raise Error city not found """

	def __init__(self,msg):
		super().__init__(msg)


class InvalidAPIKeyError(ValueError):
	""" Raise Invaldi API Key Error """

	def __init__(self,msg):
		super().__init__(msg)


class APIFileNotFoundError(FileNotFoundError):
	""" the 'weather_api_key' file not created or not found """	

	def __init__(self,msg):
		super().__init__(msg)