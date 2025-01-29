import sys
import segno
import requests
import threading
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QApplication
)


class Shorten(QWidget):

    qr_signal = pyqtSignal()
    conn_err_signal = pyqtSignal()
    invalid_url_err_signal = pyqtSignal(int)

    if __name__ == "__main__":
        import DisplayErrors
    else:
        from modules import DisplayErrors

    def __init__(self):
        super().__init__()

        self.qr_signal.connect(self.set_qr)
        self.conn_err_signal.connect(self.show_conn_err)
        self.invalid_url_err_signal.connect(self.show_URLinvalid_err)

        self.F_Layout = QVBoxLayout()
        self.qr_layout = QHBoxLayout()

        self.title = QLabel('<h2 align="center">URL SHORTENER</h2>')

        self.url = QLineEdit()
        self.url.textChanged.connect(lambda: self.short.clear())
        self.short = QLineEdit()
        self.short.setReadOnly(True)
        self.qr_label = QLabel()
        self.qr_img = QLabel()
        self.qr_img.setAlignment(Qt.AlignmentFlag.AlignJustify)

        btn = QPushButton("Submit")
        btn.clicked.connect(self.thread_shorten)

        self.qr_layout.addWidget(self.qr_label)
        self.qr_layout.addWidget(self.qr_img)
        self.qr_layout.setContentsMargins(0, 10, 0, 10)

        self.F_Layout.addWidget(self.title)
        self.F_Layout.addWidget(QLabel("<h3>Enter your URL : </h3>"))
        self.F_Layout.addWidget(self.url)
        self.F_Layout.addWidget(QLabel("<h3>Shortened URL : </h3>"))
        self.F_Layout.addWidget(self.short)
        self.F_Layout.addLayout(self.qr_layout)

        self.F_Layout.addWidget(btn)
        self.setLayout(self.F_Layout)

    def thread_shorten(self):
        self.thr = threading.Thread(target=self.shorten)
        self.thr.start()

    def shorten(self):
        url_text = self.url.text()

        try:
            response = requests.post(
                "https://api.encurtador.dev/encurtamentos", json={"url": url_text})
        except requests.exceptions.ConnectionError:
            self.conn_err_signal.emit()
        else:
            if response.status_code in (200, 201):
                self.short.setText(response.json()['urlEncurtada'])
                self.qr_maker = segno.make_qr(self.url.text())
                self.qr_maker.save(
                    'temp_qr.png',
                    scale=6,
                    border=1,
                    light='#1DE9B6'
                )
                self.qr_signal.emit()
            else:
                self.invalid_url_err_signal.emit(response.status_code)

    def set_qr(self):
        self.qr_label.setText("<h3>Scan this QR Code : </h3>")
        self.qr_img.setPixmap(QPixmap('temp_qr.png'))
        self.qr_img.setAlignment(Qt.AlignmentFlag.AlignRight)

    def show_URLinvalid_err(self, code):
        self.URLerr = self.DisplayErrors.QErrorMessage(
            f"URL Shortener Error {code}!", "Invalid URL!\nPlease enter a valid URL!")

    def show_conn_err(self):
        self.Connerr = self.DisplayErrors.QErrorMessage(
            "URL Shortener Connection Error!", "An error occured whie establishing the connection!\nPlease Try Again!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Shorten()
    window.show()
    sys.exit(app.exec())
