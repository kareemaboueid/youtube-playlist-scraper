# YouTube Playlist Scraper

A Python-based automation script that extracts video titles and durations from any public YouTube playlist using Selenium. It generates a clean and styled HTML report containing all scraped data, including metadata like script name, runtime, playlist name, and more.

## Project Structure

```txt
youtube-playlist-scraper/
├── dist/
│   ├── result.html
│   ├── script.js
│   ├── style.css
├── logs/
│   ├── log.txt
├── chromedriver.exe
├── requirements.txt
├── youtube-playlist-scraper.py
└── README.md
````

## Features

* Extracts all video titles and their durations from a YouTube playlist.
* Converts duration strings into total minutes.
* Automatically captures the playlist title.
* Generates a responsive HTML report with:

  * Script metadata (script name, elapsed time, number of videos)
  * Copy-to-clipboard functionality for each title and duration
  * One-click export to plain `.txt` format
* Automatically opens the result in your default browser
* Logs every run with timestamp, URL, script name, and processing time
* Works with or without a predefined `result.html` template (defaults to internal HTML structure if missing)

## Installation

1. Clone the repository or download the code.
2. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

**Note:** You must place the correct version of `chromedriver.exe` in the root directory. It must match your installed version of Google Chrome.

## Usage

Double-click or run the `youtube-playlist-scraper.py` file.

You’ll be prompted in the terminal to enter a YouTube playlist URL. Example format:

```
https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID
```

The script will then:

1. Launch a Chrome browser using Selenium.
2. Navigate to the playlist page.
3. Scrape all video titles and their durations.
4. Output the results to `dist/result.html`.
5. Open the report in your default browser.
6. Log session details in `logs/log.txt`.

## Requirements

* Python 3.7 or newer
* Google Chrome browser
* Matching version of ChromeDriver

## Author

Kareem Aboueid
GitHub: [https://github.com/kareemaboueid](https://github.com/kareemaboueid)
