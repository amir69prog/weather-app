
class CityNotFoundError(ValueError):
	""" Raise Error city not found """

	def __init__(self,msg):
		super().__init__(msg)

