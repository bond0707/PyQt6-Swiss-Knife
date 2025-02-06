# PyQt6 Swiss Knife

The PyQt6 Swiss Knife is an application that integrates multiple utilities into a single platform. This tool is designed with a modern GUI using PyQt6 and offers various functionalities such as email sending, language translation, Morse code conversion, PDF to audiobook conversion, URL shortening, YouTube playlist downloading, and weather scraping. This application can be compiled into executable files for windows using `nuitka` or `pyinstaller` (preferred). I have also made an executable installer for this application using `InstallForge`.

## Features

1. **Email Sender:** Send emails to multiple people at once.
2. **Language Translator:** Translate text between different languages.
3. **Morse Converter:** Encode and decode Morse code and play audio of the encoded message.
4. **PDF to Audiobook:** Convert PDF files into audiobooks.
5. **YouTube Playlist Downloader:** Download playlists from YouTube.
6. **URL Shortener:** Shorten long URLs.
7. **Weather Scraper:** Get the current weather information for a specified location.

## Usage Notes

* **General:** The functionalities provided are designed to be easy to use with a self-explanatory user interface.
* **Email Sender:** Create a text file with all the recipient email addresses, each on a new line. Use Google's temporary password for authentication.
* **Weather Scraper:** This tool scrapes data from [here](https://www.timeanddate.com/weather/ "timeanddate.com"). Users should be aware of the minimal risk of their IP being banned due to scraping this website, though this is unlikely to happen.

## Future Improvements

* [ ] Add logging functionality.
* [ ] Improve download tracking in the YouTube playlist downloader.
* [ ] Increase the size of the SwissKnife icon.
* [ ] Remove command prompts appearing when `mkvmerge.exe` is called in the YouTube playlist downloader.
* [ ] Add a line in `del_try_permissions.exe` to delete the MKVToolNix installer executable.
* [ ] Use MKVToolNix portable version instead of the installer.
* [ ] Use `icacls` command properly and use appropriate commands to edit PATH variables to enhance the installation process.
* [ ] Replace `try_permissions.exe` and `del_try_permissions.exe` with bash scripts.
