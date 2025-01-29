import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
                                QWidget, 
                                QMessageBox,
                                QApplication,
                                QDialogButtonBox
                            )

from qt_material import apply_stylesheet
from win32mica import MicaStyle, MicaTheme, ApplyMica


class QErrorMessage(QWidget):
    def __init__(self, title, message):
        super().__init__()
        self.errorDialogue=QMessageBox()        
        self.errorDialogue.setWindowIcon(QIcon(QPixmap(os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'main_icon.png')))))
                
        ApplyMica(self.errorDialogue.winId(), MicaTheme.DARK, MicaStyle.ALT)
        apply_stylesheet(self.errorDialogue,'dark_teal.xml',css_file=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','assets/modifications.css')))
        
        self.errorDialogue.setIcon(QMessageBox.Icon.Critical)
        self.errorDialogue.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.errorDialogue.setWindowTitle(title)
        self.errorDialogue.setText(message)
        
        self.errorDialogue.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.errorDialogue.findChild(QDialogButtonBox).setCenterButtons(True)
        self.errorDialogue.setModal(True)
        
        self.errorDialogue.exec()



if __name__ == "__main__":
    app=QApplication(sys.argv)
    apply_stylesheet(app,'dark_teal.xml',css_file=os.path.join(os.path.dirname(__file__),'assets/modifications.css'))
    win=QErrorMessage()
    win.show()
    sys.exit(app.exec())