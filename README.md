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
  # (No chromedriver needed)
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

Clone the repository:

```bash
git clone https://github.com/kareemaboueid/youtube-playlist-scraper.git
cd youtube-playlist-scraper
```

Install the project in editable mode:

```bash
pip install -e .
```

The command installs the application and its dependencies automatically, including Selenium.

## Usage

Run the installed command from any terminal:

```bash
scrap-youtube-course
```

You’ll be prompted to enter a YouTube playlist URL. Example format:

```
https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID
```

The command will then:

1. Launch a Chrome browser using Selenium.
2. Navigate to the playlist page.
3. Scrape all video titles and their durations.
4. Output the results to `dist/result.html`.
5. Open the report in your default browser.
6. Log session details in `logs/log.txt`.

You may also run the script directly for development:

```bash
python youtube-playlist-scraper.py
```

## Requirements

* Python 3.7 or newer
* Google Chrome browser
* Selenium 4.x or newer (for Selenium Manager)

## Author

Kareem Aboueid
GitHub: [https://github.com/kareemaboueid](https://github.com/kareemaboueid)
