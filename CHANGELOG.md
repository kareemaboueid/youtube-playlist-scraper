# Changelog

## 2026-08-11

- Refactor HTML template for cleaner structure in playlist display

## 2026-08-10

- Add modern Python packaging and editable install support with `pip install -e .`.
- Add global CLI entry point `scrap-youtube-course` that works from any terminal.
- Preserve report assets and resolve `dist/` and `logs/` relative to the installed package location.

## 2025-08-31

- Refactor `smart_scroll` function and enhance HTML template for improved playlist scraping results.
- Refactor `result.html` to enhance playlist display and update scraping details.
- Enhance styling for the result display.
- Update `chromedriver.exe` to the latest version for improved compatibility.
- Update `log.txt` with new scraping details for a YouTube playlist.

## 2025-07-08

- Initial repository setup and project scaffold.
- Added `youtube-playlist-scraper.py` for scraping YouTube playlists and generating an HTML report.
- Added `README.md` with project details and usage instructions.
- Added `requirements.txt` to specify Python dependencies.
- Added `result.html` for displaying scraped YouTube playlist details.
- Added `script.js` for copying text to clipboard and saving course details.
- Added `style.css` for layout and styling of the YouTube playlist scraper.
- Added `log.txt` to record scraping details for YouTube playlist runs.
- Added `chromedriver` executable to support Selenium browser automation.
