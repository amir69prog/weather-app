from source import QMessageBox,QFont




class CityNotFoundMessage(QMessageBox):
	""" message to say city not found """

	def __init__(self,parent,text):
		super().__init__(parent)
		self.setWindowTitle('Error 404')
		font = QFont('Verdana Pro Cond', 12)
		self.setFont(font)
		self.setText(text)
		self.setIcon(QMessageBox.Information)
		self.setStandardButtons(QMessageBox.Ok)

		self.show()