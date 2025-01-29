import os
import sys
import shutil
import pytube
import threading
from PyQt6.QtCore import pyqtSignal
from pymkv import MKVFile, MKVTrack

from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QComboBox,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QProgressBar,
    QApplication
)


class PlayistDownloader(QWidget):
    
    windows_no_print_list = ['*','/','\\','<','>',':','|','?','-','#','☺','☻','♥','♦','♣','♠','•','◘','○','◙','♂','♀','♪','♫','☼','►','◄','↕','‼','¶§','▬','↨','↑','↓','→','←','∟','↔','▲','▼']
    
    invalid_playlist_error = pyqtSignal()
    get_videos = pyqtSignal(str)
    improvise = pyqtSignal(str)
    video_num = pyqtSignal(str)
    download_pct = pyqtSignal(str)
    total_downloaded = pyqtSignal(str)
    finished = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    if __name__ == "__main__":
        import DisplayErrors
    else:
        from modules import DisplayErrors

    def __init__(self):
        super().__init__()

        self.get_videos.connect(
            lambda string: self.status_label.setText(string))

        self.invalid_playlist_error.connect(self.ShowInvalidPlaylistError)

        self.improvise.connect(
            lambda string: self.status_label.setText(string))

        self.video_num.connect(
            lambda string: self.status_label.setText(string))

        self.download_pct.connect(
            lambda string: self.progress_pct.setText(string))

        self.total_downloaded.connect(
            lambda string: self.status_label.setText(string))

        self.finished.connect(
            lambda string: self.status_label.setText(string))

        self.progress_signal.connect(
            lambda number: self.progress_bar.setValue(number))

        self.title = QLabel(
            '<h2 align="center">YOUTUBE PLAYLIST DOWNLOADER</h2>')
        self.playlist_label = QLabel("<h3>Playlist URL : </h3>")
        self.playlist_link = QLineEdit()
        self.res_label = QLabel("<h3>Resolution : </h3>")
        self.res_box = QComboBox()
        self.res_box.addItems(
            ['1080p', '720p', '480p', '360p', '240p', '144p'])
        self.download_button = QPushButton("Download")

        self.status_label = QLabel("")

        self.progress_bar = QProgressBar()
        self.progress_pct = QLabel("")

        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(self.progress_bar)
        self.Hlayout.addWidget(self.progress_pct)

        self.Vlayout = QVBoxLayout()
        self.Vlayout.addWidget(self.title)
        self.Vlayout.addWidget(self.playlist_label)
        self.Vlayout.addWidget(self.playlist_link)
        self.Vlayout.addWidget(self.res_label)
        self.Vlayout.addWidget(self.res_box)
        self.Vlayout.addWidget(self.download_button)
        self.Vlayout.addWidget(self.status_label)

        self.setLayout(self.Vlayout)

        self.download_button.clicked.connect(self.download_thread)

    def download_thread(self):
        if self.playlist_link.text() == '':
            self.invalid_playlist_error.emit()
        else:
            if hasattr(self, 'progress_bar'):
                self.Hlayout.removeWidget(self.progress_bar)
                self.Hlayout.removeWidget(self.progress_pct)
                self.progress_bar.deleteLater()
                self.progress_pct.deleteLater()
                del self.progress_bar
                del self.progress_pct

            self.progress_bar = QProgressBar(self)
            self.progress_pct = QLabel("")

            self.status_label.setText("<h3>Downloading the playlist.</h3>")
            self.Hlayout.addWidget(self.progress_bar)
            self.Hlayout.addWidget(self.progress_pct)
            self.Vlayout.addLayout(self.Hlayout)

            threading.Thread(target=self.download_playlist).start()

    def download_playlist(self):
        self.playlist_url = self.playlist_link.text()
        self.selected_resolution = self.res_box.currentText()
        self.playlist = pytube.Playlist(self.playlist_url)
        self.get_videos.emit("<h3>Fetching Videos...</h3>")

        self.progress_bar.setMinimum(0)

        try:
            self.progress_bar.setMaximum(len(self.playlist))
        except:
            self.invalid_playlist_error.emit()
        else:
            save_path = os.path.abspath(os.path.join(os.path.expanduser(
                "~\\Downloads"), "Swiss Knife", "YT Playlists", self.playlist.title))

            if not os.path.exists(save_path):
                os.makedirs(save_path, exist_ok=True)

            for i, video_link in enumerate(self.playlist):
                link = pytube.YouTube(video_link)
                
                for j in link.title:
                    if j in self.windows_no_print_list:
                        link.title = (link.title).replace(j,'-')

                self.video_num.emit(
                    f"<h3>Downloading : {link.title} ({i+1}/{len(self.playlist)})</h3>")
                
                link.streams.filter(adaptive=True, resolution=self.selected_resolution, file_extension="mp4").first().download(output_path=os.path.abspath(
                    os.path.join(os.path.expanduser("~\\Downloads"), "Swiss Knife", "YT Playlists", self.playlist.title, "Video")), skip_existing=True)

                link.streams.filter(only_audio=True, file_extension="mp4").first().download(output_path=os.path.abspath(
                    os.path.join(os.path.expanduser("~\\Downloads"), "Swiss Knife", "YT Playlists", self.playlist.title, "Audio")), skip_existing=True)
            
                final_vid = MKVFile()

                vid_track = MKVTrack(os.path.abspath(os.path.join(os.path.expanduser(
                    "~\\Downloads"), "Swiss Knife", "YT Playlists", self.playlist.title, "Video", link.title+".mp4")))
                final_vid.add_track(vid_track)

                aud_track = MKVTrack(os.path.abspath(os.path.join(os.path.expanduser(
                    "~\\Downloads"), "Swiss Knife", "YT Playlists", self.playlist.title, "Audio", link.title+".mp4")))
                final_vid.add_track(aud_track)

                final_vid.mux(os.path.abspath(os.path.join(os.path.expanduser(
                    "~\\Downloads"), "Swiss Knife", "YT Playlists", self.playlist.title, link.title+".mkv")))

                self.progress_signal.emit(i+1)
                self.download_pct.emit(
                    f"<h3>{((i+1)*100)/len(self.playlist.video_urls):.2f}%</h3>")
                self.total_downloaded.emit(
                    f"<h3>Downloaded {i + 1} of {len(self.playlist.video_urls)} videos.</h3>")

            self.finished.emit('<h3 align="center">Download complete!</h3>')

            shutil.rmtree(os.path.abspath(os.path.join(os.path.expanduser(
                "~\\Downloads"), "Swiss Knife", "YT Playlists", self.playlist.title, "Audio")))

            shutil.rmtree(os.path.abspath(os.path.join(os.path.expanduser(
                "~\\Downloads"), "Swiss Knife", "YT Playlists", self.playlist.title, "Video")))

    def ShowInvalidPlaylistError(self):
        self.PlaylistError = self.DisplayErrors.QErrorMessage(
            "Playlist Downloader Invalid URL Error!", "The URL you provided is invalid!\nPlease enter a valid youtube playlist URL!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlayistDownloader()
    window.show()
    sys.exit(app.exec())
