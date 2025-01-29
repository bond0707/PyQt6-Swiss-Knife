import sys
import threading
from PyQt6.QtCore import Qt, pyqtSignal
from deep_translator import GoogleTranslator
from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QWidget,
    QComboBox,
    QTextEdit,
    QPushButton,
    QFormLayout,
    QGridLayout,
    QApplication
)


class LanguageTranslator(QWidget):
    
    NullSourceErrorSignal = pyqtSignal()
    TranslatedSignal = pyqtSignal(str)
    ConnectionErrorSignal = pyqtSignal()

    if __name__ == "__main__":
        import DisplayErrors
    else:
        from modules import DisplayErrors

    def __init__(self):
        super().__init__()
        
        self.NullSourceErrorSignal.connect(self.DisplayNullSourceError)
        self.ConnectionErrorSignal.connect(self.DisplayConnectionError)

        self.TranslatedSignal.connect(
            lambda translated_text: self.destination.setText(translated_text))

        self.main_layout = QGridLayout()

        self.title = QLabel('<h2 align="center">LANGUAGE TRANSLATOR</h2>')

        self.translator = GoogleTranslator()

        self.lang_dict = self.translator.get_supported_languages(as_dict=True)

        self.lang_list = []
        for i in self.translator.get_supported_languages():
            self.lang_list.append(i.capitalize())

        self.source_label = QLabel('<h3 align="center">Enter your text </h3>')

        self.source = QTextEdit()
        self.source.setStyleSheet("QTextEdit{font-size: 17px;}")

        self.H_Line = QFrame()
        self.H_Line.setFrameShape(QFrame.Shape.HLine)
        self.H_Line.setFrameShadow(QFrame.Shadow.Sunken)

        self.V_Line = QFrame()
        self.V_Line.setFrameShape(QFrame.Shape.VLine)
        self.V_Line.setFrameShadow(QFrame.Shadow.Sunken)

        self.lang_box_layout = QFormLayout()

        self.lang_box_label = QLabel(
            '<h3 align="center">Choose a language </h3>')

        self.lang_box = QComboBox()
        self.lang_box.addItems(self.lang_list)
        self.lang_box.setCurrentText("English")
        self.lang_box.currentTextChanged.connect(self.SetTranslateTo)

        self.lang_box_layout.addRow(self.lang_box_label, self.lang_box)

        self.translate_info_label = QLabel(
            '<h3 align="center">Translating your text to English</h3>')

        self.translate_btn = QPushButton("Translate")
        self.translate_btn.clicked.connect(self.Translate_thread)

        self.destination = QTextEdit()
        self.destination.setReadOnly(True)
        self.destination.setStyleSheet("QTextEdit{font-size: 17px;}")

        self.source_autodetect_label = QLabel(
            '<h3 align="center">The code will auto-detect<br>the language of your source text</h3>')

        self.main_layout.addWidget(self.title, 1, 1, 1, 5)
        self.main_layout.addWidget(self.H_Line, 2, 1, 1, 5)
        self.main_layout.addWidget(self.source_label, 3, 1, 1, 2)
        self.main_layout.addWidget(self.source, 4, 1, 3, 2)
        self.main_layout.addWidget(self.V_Line, 2, 3, 5, 1)
        self.main_layout.addWidget(self.translate_info_label, 3, 4, 1, 2)
        self.main_layout.addWidget(self.destination, 4, 4, 3, 2)
        self.main_layout.addWidget(self.source_autodetect_label, 8, 1, 1, 5)
        self.main_layout.addLayout(self.lang_box_layout, 9, 1, 1, 5)
        self.main_layout.addWidget(self.translate_btn, 10, 1, 1, 5)

        self.main_layout.setSpacing(10)

        self.setLayout(self.main_layout)

    def SetTranslateTo(self, value):
        self.translator.target = value.lower()
        self.translate_info_label.setText(
            '<h3 align="center">Translating your text to ' + value + "</h3>")

    def Translate_thread(self):
        threading.Thread(target=self.Translate).start()

    def Translate(self):
        if self.source.toPlainText() == "":
            self.NullSourceErrorSignal.emit()
        else:
            try:
                self.translated_text = GoogleTranslator(
                    source="auto", target=self.translator.target).translate(self.source.toPlainText())
            except:
                self.ConnectionErrorSignal.emit()
            else:
                self.TranslatedSignal.emit(self.translated_text)

    def DisplayConnectionError(self):
        self.ConnErr = self.DisplayErrors.QErrorMessage("Language Translator Connection Error!", "An error occured whie establishing the connection!\nPlease Try Again!")
        
    def DisplayNullSourceError(self):
        self.NullSrcErr = self.DisplayErrors.QErrorMessage("Language Translator Input Error!", "Please provide some input before\nclicking the translate button!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LanguageTranslator()
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    window.show()
    sys.exit(app.exec())