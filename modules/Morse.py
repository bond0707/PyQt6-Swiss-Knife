import os
import sys
import threading
from PyQt6.QtCore import Qt, pyqtSignal
from playsound import playsound
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QButtonGroup,
    QApplication,
)


class MorseCodeEncoderDecoder(QWidget):
    
    InputErrorSignal = pyqtSignal()
    
    morse = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
        'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
        'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
        'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----',
        '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', '0': '-----', '.': '.-.-.-', ',': '--..--', '?': '..--..',
        "'": '.----.', '!': '-.-.--', '/': '-..-.', ':': '---...', ';': '-.-.-.', '=': '-...-',
        '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.', '@': '.--.-.', '(': '-.--.',
        ')': '-.--.-', '&': '.-...', '$': '...-..-', '¡': '--...-', '¿': '..-.-', ' ': '/'
    }
    
    if __name__=='__main__':
        import DisplayErrors
    else:
        from modules import DisplayErrors
    
    def __init__(self):
        super().__init__()
        
        self.InputErrorSignal.connect(self.ShowInputError)
        
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        self.title = QLabel('<h2 align="center">MORSE ENCRYPTOR/DECRYPTOR</h2>')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.encode = QRadioButton('Encoding')
        self.encode.pressed.connect(lambda : self.play_sound.setCheckable(True))
        self.encode.setChecked(True)

        self.play_sound = QCheckBox('Play Sound')

        self.decode = QRadioButton('Decoding')
        self.decode.pressed.connect(self.DisablePlaySound)

        btn_group = QButtonGroup()
        btn_group.addButton(self.encode)
        btn_group.addButton(self.decode)

        btn_layout.addWidget(self.encode)
        btn_layout.addWidget(self.play_sound)

        self.input = QLineEdit()

        self.output = QLineEdit()
        self.output.setReadOnly(True)

        self.convert = QPushButton('Encode/Decode')
        self.convert.clicked.connect(self.thread_translate)

        layout.addWidget(self.title)
        layout.addLayout(btn_layout)
        layout.addWidget(self.decode)
        layout.addWidget(QLabel('<h3>Input Text : </h3>'))
        layout.addWidget(self.input)
        layout.addWidget(QLabel('<h3>Output Text : </h3>'))
        layout.addWidget(self.output)
        layout.addWidget(self.convert)

        self.setLayout(layout)

    def thread_translate(self):
        self.thr = threading.Thread(target=self.translate)
        self.thr.start()

    def translate(self):
        input = self.input.text().upper()
        output = ''
        
        if input == '':
            self.InputErrorSignal.emit()
        else:
            if self.encode.isChecked():
                for char in input:
                    output += self.morse.get(char, '') + ' '

                self.output.setText(output)

                if self.play_sound.isChecked():
                    for i in output:
                        if i == '.':
                            playsound(os.path.abspath(os.path.join(os.path.dirname(
                                __file__), '..', 'assets', 'MorseWidget', 'dot.wav')))
                        elif i == '-':
                            playsound(os.path.abspath(os.path.join(os.path.dirname(
                                __file__), '..', 'assets', 'MorseWidget', 'dash.wav')))
                        else:
                            playsound(os.path.abspath(os.path.join(os.path.dirname(
                                __file__), '..', 'assets', 'MorseWidget', 'blank.wav')))

            else:
                cypher = input.split()

                for morse_code in cypher:
                    for key, value in self.morse.items():
                        if value == morse_code:
                            output += key

                self.output.setText(output)
                
    
    def DisablePlaySound(self):
        self.play_sound.setCheckState(Qt.CheckState.Unchecked)
        self.play_sound.setCheckable(False)
    
    
    def ShowInputError(self):
        self.InputError = self.DisplayErrors.QErrorMessage("Morse Converter Input Error!", "Please enter your message before\nclicking the encode/decode button!")



if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MorseCodeEncoderDecoder()
    window.show()
    sys.exit(app.exec())


# python -m nuitka --mingw64 --onefile --plugin-enable=pyqt6 --show-progress --follow-imports --disable-console --include-data-file=dot.wav=dot.wav --include-data-file=dash.wav=dash.wav --include-data-file=blank.wav=blank.wav --include-data-file=modifications.css=modifications.css --include-data-file=Morse.png=Morse.png --include-package-data=qt_material --windows-icon-from-ico=Morse.png Morse.py
