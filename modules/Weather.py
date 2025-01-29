import os
import sys
import requests
import threading
from bs4 import BeautifulSoup
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QSpacerItem,
    QHeaderView,
    QApplication,
    QTableWidget,
    QTableWidgetItem
)


class WeatherInfo(QWidget):

    timeout_signal = pyqtSignal()
    spelling_error_signal = pyqtSignal(int)
    content_signal = pyqtSignal(object, object)
    flag = False
    ScraperAPI = {
        'api_key': os.getenv("SCRAPER_API_KEY"),
        'url': ''
    }
    
    if __name__=='__main__':
        import DisplayErrors
    else:
        from modules import DisplayErrors


    def __init__(self):
        super().__init__()

        self.timeout_signal.connect(self.DisplayTimeoutError)
        self.spelling_error_signal.connect(lambda code : self.DisplaySpellingError(code))
        self.content_signal.connect(
            lambda response, content: self.weather(response, content))

        self.title = QLabel('<h2 align="center">WEATHER SCRAPER</h2>')

        self.country_label = QLabel("<h3>Enter Country Name : </h3>")
        self.city_label = QLabel("<h3>Enter City Name : </h3>")

        self.country = QLineEdit()
        self.city = QLineEdit()

        self.submit = QPushButton("SUBMIT")
        self.submit.clicked.connect(
            lambda: threading.Thread(target=self.get_weather).start())

        self.mainlayout = QVBoxLayout()
        self.toplayout = QVBoxLayout()
        self.bottomlayout = QVBoxLayout()

        self.toplayout.addWidget(self.title)
        self.toplayout.addWidget(self.country_label)
        self.toplayout.addWidget(self.country)
        self.toplayout.addWidget(self.city_label)
        self.toplayout.addWidget(self.city)
        self.toplayout.addWidget(self.submit)

        self.toplayout.setContentsMargins(0, 3, 3, 4)
        self.bottomlayout.setContentsMargins(0, 3, 3, 4)

        self.mainlayout.addLayout(self.toplayout)
        self.mainlayout.addLayout(self.bottomlayout)
        self.mainlayout.insertSpacerItem(1, QSpacerItem(2, 3))
        self.setLayout(self.mainlayout)


    def get_weather(self):
        self.ScraperAPI.update(
            {'url': 'https://www.timeanddate.com/weather/'+self.country.text()+'/'+self.city.text()})
        try:
            response = requests.get(
                'http://api.scraperapi.com', params=self.ScraperAPI)
            content = BeautifulSoup(response.text, 'html.parser')
        except:
            self.timeout_signal.emit()
        else:
            self.content_signal.emit(response, content)


    def weather(self, response, content):
        if self.flag is True:
            for i in reversed(range(self.bottomlayout.count())):
                self.bottomlayout.itemAt(i).widget().setParent(None)

        try:
            content.find(class_='h2').get_text()
        except:
            self.spelling_error_signal.emit(response.status_code)
            self.flag = True
        else:
            self.bottomlayout.addWidget(QLabel(
                f'<h3 align="center">Weather in {self.city.text().capitalize()}, {self.country.text().capitalize()}</h3>'))

            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(['Fields', 'Readings'])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            table.insertRow(table.rowCount())
            table.setItem(table.rowCount()-1, 0,
                          QTableWidgetItem("Temperature:"))
            table.setItem(table.rowCount()-1, 1,
                          QTableWidgetItem(content.find(class_='h2').get_text()))

            for i in range(1, 7):
                table.insertRow(table.rowCount())
                table.setItem(
                    table.rowCount()-1, 0, QTableWidgetItem(content.find_all('th')[i].get_text()))
                table.setItem(
                    table.rowCount()-1, 1, QTableWidgetItem(content.find_all('td')[i].get_text()))

            table.setBaseSize(580, 300)
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.bottomlayout.addWidget(table)

            self.flag = True
            
        
    def DisplayTimeoutError(self):
        self.TimeoutError = self.DisplayErrors.QErrorMessage("Weather App Connection Error!", "An error occured whie establishing the connection!\nPlease Try Again!")
        
    
    def DisplaySpellingError(self, code):
        self.SpellingError = self.DisplayErrors.QErrorMessage(f"Weather Scraper Error {code}!", "The provided location is invalid!\nCheck your spelling and try again!")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherInfo()
    window.show()
    sys.exit(app.exec())
