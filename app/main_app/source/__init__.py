import sys
import os

from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from .api import IconStateWeatherAPI, CityWeatherAPI
from .exceptions import CityNotFoundError