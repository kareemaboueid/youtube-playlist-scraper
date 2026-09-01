# Changelog

## 2026-09-02

- Fix stale playlist data being reused between executions of the global `scrap-youtube-course` command.
- Fix resource path resolution so generated reports and logs resolve to the correct repository locations without malformed paths such as `scrap_youtube_course..`.
- Refactor the project so `scrap_youtube_course/main.py` is the single authoritative scraper implementation.
- Reduce `youtube-playlist-scraper.py` to a thin compatibility/development wrapper that delegates to the package entry point.
- Add protection against using an already-generated `result.html` as the next scraping template.
- Update `.gitignore` to exclude generated runtime files such as `dist/result.html` and `logs/log.txt`.
- Remove generated runtime files from Git tracking while keeping them available locally.
- Update README documentation to reflect the current package structure and Python 3.10+ requirement.
- Preserve the existing HTML report design and ensure `script.js` and `style.css` remain unchanged.

## 2026-08-11

- Improve text copying functionality by sanitizing whitespace before copying to clipboard
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
