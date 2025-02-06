import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QApplication,
    QStackedLayout
)

from qt_material import apply_stylesheet
from win32mica import MicaTheme, MicaStyle, ApplyMica

from modules import (
    Morse,
    Weather,
    Shortener,
    Downloader,
    Translator,
    EmailSender,
    PdfToAudiobook,
)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.resize(868, 608)
        self.setWindowTitle("PyQt6 Swiss Knife by Kirtan")
        self.setWindowIcon(QIcon(QPixmap(os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'assets', 'main_icon.png')))))

        self.mainlayout = QGridLayout()
        self.seperator = QFrame()
        self.leftlayout = QVBoxLayout()
        self.rightlayout = QStackedLayout()

        self.seperator.setFrameShape(QFrame.Shape.VLine)
        self.seperator.setFrameShadow(QFrame.Shadow.Sunken)

        self.mainlayout.addLayout(self.leftlayout, 0, 0, 4, 1)
        self.mainlayout.addWidget(self.seperator, 0, 1, 4, 1)
        self.mainlayout.addLayout(self.rightlayout, 0, 2, 4, 3)
        self.mainlayout.setContentsMargins(10, 10, 10, 10)
        self.mainlayout.setHorizontalSpacing(20)

        self.Email = EmailSender.SendMail()
        self.Translate = Translator.LanguageTranslator()
        self.Morse = Morse.MorseCodeEncoderDecoder()
        self.Audiobook = PdfToAudiobook.AudioBook()
        self.URL = Shortener.Shorten()
        self.Download = Downloader.PlayistDownloader()
        self.Weather = Weather.WeatherInfo()

        self.setLayout(self.mainlayout)

        self.initUI()

    def initUI(self):
        self.Emailbtn = QPushButton("E-mail Sender")
        self.leftlayout.addWidget(self.Emailbtn)
        self.Emailbtn.clicked.connect(
            lambda: self.rightlayout.setCurrentWidget(self.Email))

        self.Translatebtn = QPushButton("Language Translator")
        self.leftlayout.addWidget(self.Translatebtn)
        self.Translatebtn.clicked.connect(
            lambda: self.rightlayout.setCurrentWidget(self.Translate))

        self.Morsebtn = QPushButton("Morse Converter")
        self.leftlayout.addWidget(self.Morsebtn)
        self.Morsebtn.clicked.connect(
            lambda: self.rightlayout.setCurrentWidget(self.Morse))

        self.Audiobtn = QPushButton("PDF To Audiobook")
        self.leftlayout.addWidget(self.Audiobtn)
        self.Audiobtn.clicked.connect(
            lambda: self.rightlayout.setCurrentWidget(self.Audiobook))

        self.Downloadbtn = QPushButton("Playlist Downloader")
        self.leftlayout.addWidget(self.Downloadbtn)
        self.Downloadbtn.clicked.connect(
            lambda: self.rightlayout.setCurrentWidget(self.Download))

        self.URLbtn = QPushButton("URL Shortener")
        self.leftlayout.addWidget(self.URLbtn)
        self.URLbtn.clicked.connect(
            lambda: self.rightlayout.setCurrentWidget(self.URL))

        self.Weatherbtn = QPushButton("Weather Scraper")
        self.leftlayout.addWidget(self.Weatherbtn)
        self.Weatherbtn.clicked.connect(
            lambda: self.rightlayout.setCurrentWidget(self.Weather))

        self.rightlayout.addWidget(self.Email)
        self.rightlayout.addWidget(self.Translate)
        self.rightlayout.addWidget(self.Morse)
        self.rightlayout.addWidget(self.Audiobook)
        self.rightlayout.addWidget(self.URL)
        self.rightlayout.addWidget(self.Download)
        self.rightlayout.addWidget(self.Weather)


if __name__ == '__main__':
    if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets", "try_permissions.exe"))):
        os.remove(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "assets", "try_permissions.exe")))
        
    if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets", "del_try_permissions.exe"))):
        os.remove(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "assets", "del_try_permissions.exe")))
        
    app = QApplication(sys.argv)
    apply_stylesheet(app, 'dark_teal.xml', css_file=os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'assets/modifications.css')))

    window = MainWindow()
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    ApplyMica(window.winId(), MicaTheme.AUTO, MicaStyle.ALT)
    window.show()

    sys.exit(app.exec())


# TO COMPILE USING NUITKA:
# python -m nuitka --mingw64 --standalone --plugin-enable=pyqt6 --show-progress --follow-imports --include-package-data=qt_material --disable-console --windows-icon-from-ico="C:\Me\Notes\Semester 3\Python\Micro Project\Swiss Knife\assets\main_icon.png" main_layout.py

# TO COMPILE USING PYINSTALLER:
# pyinstaller --onedir --noconsole --icon="C:\Me\Notes\Semester 3\Python\Micro Project\Swiss Knife\assets\main_icon.png" SwissKnife.py

