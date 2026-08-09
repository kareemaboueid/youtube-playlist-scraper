import html
import os
import re
import sys
import time
import traceback
import webbrowser
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="./style.css" />
    <title>%SCRIPT_NAME%</title>
</head>
<body>
    <section class="result_wrapper">
        <div class="result_top">
            <section class="result_header">
                <div>
                    <h1>YouTube playlist successfully scraped</h1>
                </div>
                <div class="result_header_actions">
                    <button onclick="save_to_file()">Save</button>
                    <button onclick="window.close()">Exit</button>
                </div>
            </section>

            <div class="result_info">
                <div class="info_details">
                    <p>
                        <strong>Script: </strong>
                        <a
                            href="https://github.com/kareemaboueid/youtube-playlist-scraper"
                            target="_blank"
                        >
                            %SCRIPT_NAME%
                        </a>
                    </p>

                    <p>
                        <strong>Time: </strong>
                        <span id="scraping_time">%TIME_TAKEN%</span>s
                    </p>

                    <p>
                        <strong>length: </strong>%DATA_LENGTH%
                    </p>

                    <p>
                        <strong>Playlist: </strong>
                        <a
                            style="cursor: pointer;"
                            onclick="window.open('%SCRAPING_URL%', '_blank')"
                        >
                            Open ↗
                        </a>
                    </p>
                </div>

                <br />

                <div class="data_header">
                    <div class="title">
                        <p>Playlist Title</p>
                    </div>

                    <div class="duration">
                        <p>Playlist Duration</p>
                    </div>
                </div>

                <div class="result_body">
                    <div class="single_data_section">
                        <div class="title" title="Click to copy">
                            <a onclick="copy_text(this)" class="txt">
                                %PLAYLIST_NAME%
                            </a>
                        </div>

                        <div class="duration" title="Click to copy">
                            <p onclick="copy_text(this)" class="txt">
                                %PLAYLIST_TOTAL_DURATION%
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="result_body">%ALL_DATA%</div>
    </section>

    <footer>
        <p>
            Made by
            <a href="https://github.com/kareemaboueid">
                Kareem Aboueid
            </a>
        </p>
    </footer>

    <script src="./script.js"></script>
</body>
</html>
'''

VIDEO_CONTAINER_SELECTOR = "div.ytLockupViewModelHost.ytLockupViewModelHorizontal"
PLAYLIST_TITLE_SELECTOR = "ytd-playlist-header-renderer yt-formatted-string#text"
PLAYLIST_TITLE_FALLBACK = "ytd-playlist-header-renderer yt-dynamic-sizing-formatted-string"
VIDEO_TITLE_SELECTOR = "a.ytLockupMetadataViewModelTitle"
VIDEO_TITLE_FALLBACK = "a[href*='/watch?v=']"
VIDEO_DURATION_SELECTOR = "a.ytLockupViewModelContentImage"
DURATION_PATTERN = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")


def print_agent(msg: str, prefix: str = "MSG: ") -> None:
    print(f"{prefix}{msg}")


def is_valid_playlist_url(url: str) -> bool:
    if not url:
        return False
    try:
        parsed = urlparse(url.strip())
    except Exception:
        return False

    if parsed.scheme not in {"http", "https"}:
        return False

    hostname = (parsed.hostname or "").lower()
    if "youtube.com" not in hostname:
        return False

    query = parse_qs(parsed.query)
    return bool(query.get("list"))


def create_browser() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=options)


def wait_for_playlist_page(driver: webdriver.Chrome) -> None:
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ytd-playlist-header-renderer")
            )
        )
    except TimeoutException as exc:
        raise RuntimeError("Unable to load playlist page header.") from exc


def get_playlist_title(driver: webdriver.Chrome, fallback: str) -> str:
    selectors = [PLAYLIST_TITLE_SELECTOR, PLAYLIST_TITLE_FALLBACK]
    for selector in selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            text = element.text.strip()
            if text:
                return text
        except NoSuchElementException:
            continue
    return fallback


def get_video_containers(driver: webdriver.Chrome) -> list[webdriver.remote.webelement.WebElement]:
    try:
        return driver.find_elements(By.CSS_SELECTOR, VIDEO_CONTAINER_SELECTOR)
    except Exception:
        return []


def find_title_in_container(container: webdriver.remote.webelement.WebElement) -> tuple[str, str] | None:
    try:
        title_element = container.find_element(
            By.CSS_SELECTOR, VIDEO_TITLE_SELECTOR)
        title = title_element.text.strip()
        href = title_element.get_attribute("href") or ""
        if title:
            return title, href
    except NoSuchElementException:
        pass

    try:
        fallback_elements = container.find_elements(
            By.CSS_SELECTOR, VIDEO_TITLE_FALLBACK)
        for elem in fallback_elements:
            title = elem.text.strip()
            if title:
                href = elem.get_attribute("href") or ""
                return title, href
    except Exception:
        pass

    return None


def find_duration_in_container(container: webdriver.remote.webelement.WebElement) -> str | None:
    try:
        duration_element = container.find_element(
            By.CSS_SELECTOR, VIDEO_DURATION_SELECTOR)
        duration_text = duration_element.text.strip()
        if DURATION_PATTERN.fullmatch(duration_text):
            return duration_text
    except NoSuchElementException:
        pass
    except StaleElementReferenceException:
        pass

    try:
        descendants = container.find_elements(By.CSS_SELECTOR, "*")
        for descendant in descendants:
            text = descendant.text.strip()
            if DURATION_PATTERN.search(text):
                match = DURATION_PATTERN.search(text)
                if match:
                    return match.group(0)
    except StaleElementReferenceException:
        pass
    except Exception:
        pass

    return None


def normalize_video_url(url: str) -> str:
    if not url:
        return ""
    if url.startswith("/"):
        return urljoin("https://www.youtube.com", url)
    return url


def scroll_to_bottom(driver: webdriver.Chrome, container: webdriver.remote.webelement.WebElement | None) -> None:
    if container is not None:
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'auto', block: 'end'});",
                container,
            )
            return
        except Exception:
            pass
    driver.execute_script("window.scrollBy(0, window.innerHeight * 0.8);")


def load_all_video_containers(driver: webdriver.Chrome) -> list[webdriver.remote.webelement.WebElement]:
    stable_attempts = 3
    max_attempts = 20
    pause_time = 1.0

    previous_count = 0
    stable_count = 0

    for attempt in range(1, max_attempts + 1):
        containers = get_video_containers(driver)
        current_count = len(containers)

        if current_count == 0 and attempt == 1:
            time.sleep(2)
            containers = get_video_containers(driver)
            current_count = len(containers)

        if current_count > previous_count:
            stable_count = 0
            previous_count = current_count
        else:
            stable_count += 1

        if stable_count >= stable_attempts:
            break

        last_container = containers[-1] if containers else None
        scroll_to_bottom(driver, last_container)
        time.sleep(pause_time)

    return get_video_containers(driver)


def convert_duration_to_minutes(duration_text: str | int) -> int:
    if duration_text is None:
        return 0
    if isinstance(duration_text, int):
        return duration_text

    if not duration_text:
        return 0

    parts = duration_text.strip().split(":")
    try:
        if len(parts) == 3:
            hours, minutes, seconds = parts
            total_seconds = int(hours) * 3600 + \
                int(minutes) * 60 + int(seconds)
            return round(total_seconds / 60)
        if len(parts) == 2:
            minutes, seconds = parts
            total_seconds = int(minutes) * 60 + int(seconds)
            return round(total_seconds / 60)
    except ValueError:
        return 0

    return 0


def extract_video_records(driver: webdriver.Chrome) -> list[dict[str, str | int]]:
    containers = get_video_containers(driver)
    records: list[dict[str, str | int]] = []
    seen_ids: set[str] = set()
    index = 0

    for container in containers:
        try:
            title_data = find_title_in_container(container)
            if title_data is None:
                continue

            title, href = title_data
            url = normalize_video_url(href)
            duration_text = find_duration_in_container(container)
            if not duration_text:
                continue

            duration = convert_duration_to_minutes(duration_text)
            identifier = url or f"{title}|{duration_text}"
            if identifier in seen_ids:
                continue

            seen_ids.add(identifier)
            index += 1
            records.append(
                {
                    "index": index,
                    "title": title,
                    "duration": duration,
                    "url": url,
                }
            )
        except StaleElementReferenceException:
            continue
        except Exception:
            continue

    return records


def build_html_report(
    script_name: str,
    url: str,
    playlist_title: str,
    playlist_total_duration: int,
    video_count: int,
    videos: list[dict[str, str | int]],
    template_path: str | None = None,
    elapsed_time: float = 0.0,
) -> str:
    if template_path and os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    else:
        template = DEFAULT_TEMPLATE

    html_snippets = []
    for video in videos:
        safe_title = html.escape(str(video["title"]))
        safe_duration = html.escape(str(video["duration"]))
        html_snippets.append(
            f'''
                <div class="single_data_section">
                    <div class="title" title="Click to copy">
                        <p onclick="copy_text(this)" class="txt">({video['index']}) {safe_title}</p>
                    </div>
                    <div class="duration" title="Click to copy">
                        <p onclick="copy_text(this)" class="txt">{safe_duration}</p>
                    </div>
                </div>
            '''
        )

    html_content = (
        template
        .replace("%SCRIPT_NAME%", html.escape(script_name))
        .replace("%TIME_TAKEN%", f"{elapsed_time}")
        .replace("%SCRAPING_URL%", html.escape(url, quote=True))
        .replace("%PLAYLIST_NAME%", html.escape(playlist_title))
        .replace("%PLAYLIST_TOTAL_DURATION%", str(playlist_total_duration))
        .replace("%DATA_LENGTH%", str(video_count))
        .replace("%ALL_DATA%", "\n".join(html_snippets))
    )
    return html_content


def save_report(content: str, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def append_log(script_name: str, url: str, video_count: int, elapsed: float) -> None:
    os.makedirs("./logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log_entry = f"[{timestamp}] {script_name} {url} length={video_count} time={elapsed}sec\n"
    with open("./logs/log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)


def scrape_playlist(url: str) -> None:
    script_name = os.path.basename(__file__)
    start_time = time.time()
    driver = None
    video_count = 0
    videos: list[dict[str, str | int]] = []

    if not is_valid_playlist_url(url):
        raise ValueError("Invalid YouTube playlist URL.")

    try:
        print_agent("Launching browser...")
        driver = create_browser()

        print_agent("Opening playlist...")
        driver.get(url)

        wait_for_playlist_page(driver)
        WebDriverWait(driver, 30).until(
            lambda d: len(get_video_containers(d)) > 0
        )

        print_agent("Loading playlist videos...")
        load_all_video_containers(driver)

        print_agent("Extracting playlist data...")
        videos = extract_video_records(driver)
        if not videos:
            raise RuntimeError("No playlist video records could be extracted.")

        playlist_title = get_playlist_title(driver, url)
        video_count = len(videos)
        playlist_total_duration = sum(
            convert_duration_to_minutes(video["duration"])
            for video in videos
        )
        elapsed_time = round(time.time() - start_time, 2)

        html_content = build_html_report(
            script_name=script_name,
            url=url,
            playlist_title=playlist_title,
            playlist_total_duration=playlist_total_duration,
            video_count=video_count,
            videos=videos,
            template_path="./result.html",
            elapsed_time=elapsed_time,
        )

        output_path = "./dist/result.html"
        save_report(html_content, output_path)
        print_agent(f"HTML report saved to '{output_path}'")

        try:
            webbrowser.open_new_tab(os.path.abspath(output_path))
            print_agent("Report opened in browser.")
        except Exception as exc:
            print_agent(f"Failed to open report: {exc}", prefix="WARNING: ")

    except Exception as exc:
        print_agent("An error occurred during scraping.")
        print_agent(str(exc), prefix="ERROR: ")
        traceback.print_exc()
    finally:
        elapsed = round(time.time() - start_time, 2)
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass
        append_log(script_name, url, video_count, elapsed)
        print_agent(f"Total processing time: {elapsed}s")


if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ").strip()
    scrape_playlist(playlist_url)
