import os
import sys
import pyttsx3
import threading
from pyttsx3 import *
from pathlib import Path
from pypdf import PdfReader
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QSlider,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QApplication
)


class AudioBook(QWidget):
    
    no_path_signal = pyqtSignal()
    success_signal = pyqtSignal()

    if __name__=='__main__':
        import DisplayErrors
    else:
        from modules import DisplayErrors
        
    def __init__(self):
        super().__init__()

        self.success_signal.connect(self.tell_success)
        self.no_path_signal.connect(self.ShowNoPathError)
        
        self.mainLayout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        self.title = QLabel('<h2 align="center">AUDIOBOOK MAKER</h2>')
        self.pdf_btn = QPushButton("Select PDF")
        self.pdf_label = QLineEdit()
        self.voice_label = QLabel("<h3>Choose Voice : </h3>")
        self.male_voice = QRadioButton("Male")
        self.female_voice = QRadioButton("Female")
        self.make_book = QPushButton("Make Audiobook")
        self.rate_label = QLabel("<h3>Rate of Speech : 200 words/minute</h3>")
        self.rate_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_label = QLabel("<h3>Volume : 25%</h3>")
        self.volume_slider = QSlider()
        self.success_label = QLabel("")

        self.title.setMargin(15)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pdf_label.setPlaceholderText("Path to your PDF file...")
        self.pdf_label.setReadOnly(True)

        self.male_voice.setChecked(True)

        self.rate_slider.setMinimum(50)
        self.rate_slider.setMaximum(1000)
        self.rate_slider.setValue(200)
        self.rate_slider.valueChanged.connect(lambda: self.rate_label.setText(
            f"<h3>Rate of Speech : {self.rate_slider.value()} words/minute</h3>"))

        self.volume_slider.setOrientation(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(30)
        self.volume_slider.valueChanged.connect(lambda: self.volume_label.setText(
            f"<h3>Volume : {self.volume_slider.value()}%</h3>"))

        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.male_voice)
        self.btn_group.addButton(self.female_voice)

        self.btn_layout.addWidget(self.male_voice)
        self.btn_layout.addWidget(self.female_voice)

        self.mainLayout.addWidget(self.title)
        self.mainLayout.addWidget(self.pdf_btn)
        self.mainLayout.addWidget(self.pdf_label)
        self.mainLayout.addWidget(self.voice_label)
        self.mainLayout.addLayout(self.btn_layout)
        self.mainLayout.addWidget(self.rate_label)
        self.mainLayout.addWidget(self.rate_slider)
        self.mainLayout.addWidget(self.volume_label)
        self.mainLayout.addWidget(self.volume_slider)
        self.mainLayout.addWidget(self.make_book)

        self.pdf_btn.clicked.connect(self.Selector)
        self.make_book.clicked.connect(self.MakeAudioBook_thread)

        self.setLayout(self.mainLayout)

    def Selector(self):
        self.file = QFileDialog()
        self.file.setFileMode(QFileDialog.FileMode.ExistingFiles)
        self.file.setNameFilter("PDFs (*.pdf)")

        if self.file.exec():
            self.file_path = self.file.selectedFiles()[0]
            self.pdf_label.setText(self.file_path)

    def MakeAudioBook_thread(self):
        threading.Thread(target=self.MakeAudioBook).start()

    def MakeAudioBook(self):
        try:
            self.pdf = PdfReader(self.file_path)
        except AttributeError:
            self.no_path_signal.emit()
        else:
            self.pdfname = ''
            for i in self.file_path[::-1]:
                if i == '/':
                    break
                self.pdfname += i

            self.pdfname = self.pdfname[::-1][:len(self.pdfname)-4]

            self.voice = pyttsx3.init()
            self.content = ""

            self.voice_type = self.voice.getProperty('voices')
            self.voice_volume = self.voice.getProperty('volume')
            self.voice.setProperty('volume', (self.volume_slider.value()*10)/1000)

            if self.male_voice.isChecked():
                self.voice.setProperty('voice', self.voice_type[0].id)
            else:
                self.voice.setProperty('voice', self.voice_type[1].id)

            self.voice.setProperty('rate', self.rate_slider.value())

            for i in range(len(self.pdf.pages)):
                current_page = self.pdf.pages[i]
                self.content += current_page.extract_text()
                
            downloads_path = str(Path.home() / "Downloads")
            save_path = os.path.abspath(os.path.join(downloads_path,"Swiss Knife","Audiobooks"))
            
            if not os.path.exists(save_path):
                os.makedirs(save_path, exist_ok=True)

            audiobook_path = os.path.abspath(os.path.join(save_path, self.pdfname+"-Audiobook.mp3"))
            self.voice.save_to_file(text=self.content, filename=audiobook_path)

            self.voice.runAndWait()
            self.success_signal.emit()

    def tell_success(self):
        if hasattr(self.mainLayout, "success_widget"):
            self.success_label.setText('<h3 align="center">'+self.pdfname+'-Audiobook.mp3' +
                                       ' successfully created and stored in Audiobooks folder!</h3>')
        else:
            self.mainLayout.addWidget(self.success_label)
            self.success_label.setText('<h3 align="center">'+self.pdfname+'-Audiobook.mp3' +
                                       ' successfully created and stored in Audiobooks folder!</h3>')
            
    
    def ShowNoPathError(self):
        self.NoPathError = self.DisplayErrors.QErrorMessage("Audiobook Maker Selection Error!", "Please select a PDF file\nbefore making an Audiobook!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioBook()
    window.show()
    sys.exit(app.exec())
