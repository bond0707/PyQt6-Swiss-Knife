import sys
import smtplib
import threading
from email.message import EmailMessage
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QWidget,
    QLineEdit,
    QTextEdit,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QApplication
)


class SendMail(QWidget):

    LoginErrorSignal = pyqtSignal()
    ConnectionFailureSignal = pyqtSignal()
    UnknownErrorSignal = pyqtSignal()
    AfterLoginSignal = pyqtSignal()
    SuccessSignal = pyqtSignal()

    if __name__ == "__main__":
        import DisplayErrors
    else:
        from modules import DisplayErrors

    def __init__(self):
        super().__init__()

        self.LoginErrorSignal.connect(self.ShowLoginError)
        self.ConnectionFailureSignal.connect(self.ShowConnectionError)
        self.UnknownErrorSignal.connect(self.ShowUnknownError)
        self.AfterLoginSignal.connect(self.AfterLogin)
        self.SuccessSignal.connect(lambda: self.logout_layout.addWidget(
            QLabel('<h3 align="center">E-mails Sent!</h3>')))

        self.main_layout = QVBoxLayout()
        self.login_layout = QVBoxLayout()

        self.title = QLabel('<h2 align="center">AUTOMATIC E-MAIL SENDER</h2>')
        self.user_label = QLabel("<h3>Enter your E-mail : </h3>")
        self.user_widget = QLineEdit()
        self.pass_label = QLabel("<h3>Enter your Password : </h3>")
        self.pass_widget = QLineEdit()
        self.pass_widget.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_btn = QPushButton("Log-In")
        self.login_btn.clicked.connect(self.OnLogin_Thread)

        self.login_layout.addWidget(self.title)
        self.login_layout.addWidget(self.user_label)
        self.login_layout.addWidget(self.user_widget)
        self.login_layout.addWidget(self.pass_label)
        self.login_layout.addWidget(self.pass_widget)
        self.login_layout.addWidget(self.login_btn)

        self.logout_layout = QVBoxLayout()
        
        self.file = None
        
        self.select_btn = QPushButton(
            "Select File Containing Recipient E-mails")
        self.select_btn.clicked.connect(self.SelectRecipients)
        self.txt_path = QLineEdit()
        self.txt_path.setPlaceholderText("Path to your text file...")
        self.txt_path.setReadOnly(True)

        self.grid_layout = QGridLayout()

        self.subject_label = QLabel("<h3>Subject : </h3>")
        self.subject = QLineEdit()
        self.content_label = QLabel("<h3>Body : </h3>")
        self.content = QTextEdit()
        self.sendmail = QPushButton("Send")
        self.sendmail.clicked.connect(self.GetMails)
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.AfterLogout)
        
        self.SendLogoutLayout = QHBoxLayout()
        self.SendLogoutLayout.addWidget(self.logout_btn)
        self.SendLogoutLayout.addWidget(self.sendmail)

        self.grid_layout.addWidget(self.subject_label, 1, 0)
        self.grid_layout.addWidget(self.subject, 1, 1)
        self.grid_layout.addWidget(self.content_label, 2, 0)
        self.grid_layout.addWidget(self.content, 2, 1, 5, 1)
        self.grid_layout.addLayout(self.SendLogoutLayout, 8, 0, 1, 2)

        self.logout_layout.addWidget(self.select_btn)
        self.logout_layout.addWidget(self.txt_path)
        self.logout_layout.addLayout(self.grid_layout)

        self.first_frame = QFrame()
        self.first_frame.setLayout(self.login_layout)
        self.first_frame.setStyleSheet(
            "QFrame {background:transparent; border: none}")

        self.second_frame = QFrame()
        self.second_frame.setLayout(self.logout_layout)
        self.second_frame.setStyleSheet(
            "QFrame {background:transparent; border: none} QTextEdit {background-color: #232629; border: 2px solid #226255}")

        self.main_layout.addWidget(self.first_frame)
        self.main_layout.addWidget(self.second_frame)

        self.second_frame.hide()

        self.setLayout(self.main_layout)


    def OnLogin_Thread(self):
        threading.Thread(target=self.Login).start()


    def Login(self):
        try:
            self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            self.server.login(self.user_widget.text(), self.pass_widget.text())
        except (smtplib.SMTPHeloError, smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
            self.ConnectionFailureSignal.emit()
        except smtplib.SMTPAuthenticationError:
            self.LoginErrorSignal.emit()
        except:
            self.UnknownErrorSignal.emit()
        else:
            self.username = self.user_widget.text()
            self.AfterLoginSignal.emit()


    def AfterLogin(self):
        self.first_frame.hide()
        self.second_frame.show()


    def SelectRecipients(self):
        self.file = QFileDialog()
        self.file.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.file.setNameFilter("Text Document (*.txt)")

        if self.file.exec():
            self.txt_path.setText(self.file.selectedFiles()[0])


    def GetMails(self):
        try:
            f = open(self.file.selectedFiles()[0], 'r')
        except:
            self.NoFileError = self.DisplayErrors.QErrorMessage("No Recipient E-mails!", "Select a Text File First!")
        else:
            self.all_mails = [line.strip() for line in f]
            threading.Thread(target=self.AutomateMails).start()


    def AutomateMails(self):
        try:
            for mail in self.all_mails:
                message = EmailMessage()
                message['From'] = self.username
                message['To'] = mail
                message['Subject'] = self.subject.text()
                message.set_content(self.content.toPlainText())
                self.server.send_message(message)
        except (smtplib.SMTPHeloError, smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
            self.ConnectionFailureSignal.emit()
        except:
            self.UnknownErrorSignal.emit()
        else:
            self.SuccessSignal.emit()


    def AfterLogout(self):
        try:
            self.server.quit()
        except smtplib.SMTPServerDisconnected:
            pass

        self.user_widget.clear()
        self.pass_widget.clear()
        self.subject.clear()
        self.content.clear()
        self.txt_path.clear()

        try:
            self.file.deleteLater()
        except (RuntimeError, AttributeError):
            pass

        self.second_frame.hide()
        self.first_frame.show()


    def ShowLoginError(self):
        self.LoginError = self.DisplayErrors.QErrorMessage("E-mail Sender Login Error!", "Invalid Credentials! Please Try Again!")


    def ShowConnectionError(self):
        self.ConnectionError = self.DisplayErrors.QErrorMessage("E-mail Sender Connection Error", "An error occured whie establishing the connection!\nPlease login again!")


    def ShowUnknownError(self):
        self.UnknownError = self.DisplayErrors.QErrorMessage("E-mail Sender Unknown Error", "An unknown error occured!\nPlease try again!")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SendMail()
    window.show()
    sys.exit(app.exec())