# youtube-playlist-scraper.py
# Version 2.0
# @Author: Kareem Aboueid https://github.com/kareemaboueid

import os
import time
import webbrowser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException


def print_agent(msg, prefix="MSG: "):
    print(f"{prefix}{msg}")


def convert_duration_to_minutes(duration_text):
    try:
        parts = duration_text.strip().split(':')
        if len(parts) == 3:
            h, m, _ = map(int, parts)
            return h * 60 + m
        elif len(parts) == 2:
            m, _ = map(int, parts)
            return m
        else:
            return 0
    except:
        return 0


def smart_scroll(driver, pause_time=0.1, cycles=1):
    height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    for _ in range(cycles):
        for i in range(0, height, 900):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(pause_time)
    driver.execute_script(
        "window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(0.2)


default_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="./style.css" />
    <title>%SCRIPT_NAME%</title>
</head>
<body>
    <section class="result_wrapper">
        <section class="result_header">
            <div>
                <h1>YouTube playlist successfully scraped</h1>
            </div>
            <div class="result_header_actions">
                <button onclick="save_to_file()">Save</button>
                <button onclick="window.close()">Close</button>
            </div>
        </section>
        <div class="result_info">
            <div class="info_details">
                <p><strong>Script: </strong>%SCRIPT_NAME%</p>
                <p><strong>Time: </strong><span id="scraping_time">%TIME_TAKEN%</span>s</p>
                <p><strong>length: </strong>%DATA_LENGTH%</p>
            </div>
            <div class="info_details">
                <p><strong>Playlist: </strong><a href="%SCRAPING_URL%">%PLAYLIST_NAME%</a></p>
            </div>
        </div>
        <div class="separator"></div>
        <div class="data_header">
            <div class="title"><p>Title</p></div>
            <div class="duration"><p>Duration</p></div>
        </div>
        <div class="result_body">%ALL_DATA%</div>
    </section>
    <footer>
        <p>Made by <a href="https://github.com/kareemaboueid">Kareem Aboueid</a></p>
    </footer>
    <script src="./script.js"></script>
</body>
</html>
'''


def scrape_playlist(url, chromedriver_path="./chromedriver.exe"):
    start_time = time.time()
    script_name = os.path.basename(__file__)
    video_count = 0
    elapsed = 0

    if not url.startswith("https://www.youtube.com/playlist?list="):
        print("Invalid YouTube playlist URL.")
        exit(1)

    print_agent("Launching browser...")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
    except WebDriverException as e:
        print_agent("ChromeDriver failed to launch.")
        print(e)
        return

    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "video-title")))
        time.sleep(1)

        print_agent("Scrolling to load full playlist...")
        smart_scroll(driver)

        playlist_title = driver.find_element(
            By.CLASS_NAME, "yt-dynamic-sizing-formatted-string").text.strip()
        title_elements = driver.find_elements(By.ID, "video-title")
        duration_elements = driver.find_elements(
            By.CLASS_NAME, "ytd-thumbnail-overlay-time-status-renderer")

        title_texts = [el.get_attribute("title").strip(
        ) for el in title_elements if el.get_attribute("title")]
        duration_texts = [el.text.strip()
                          for el in duration_elements if el.text.strip()]
        durations = [convert_duration_to_minutes(d) for d in duration_texts]

        videos = list(zip(title_texts, durations))[:len(title_texts)]
        video_count = len(videos)

        html_snippets = []
        for idx, (title, minutes) in enumerate(videos, 1):
            html_snippets.append(f'''
                <div class="single_data_section">
                    <div class="title" title="Click to copy">
                        <p onclick="copy_text(this)" class="txt">({idx}) {title}</p>
                    </div>
                    <div class="duration" title="Click to copy">
                        <p onclick="copy_text(this)" class="txt">{minutes}</p>
                    </div>
                </div>
            ''')

        os.makedirs("./dist", exist_ok=True)
        template_path = "./result.html"
        output_path = "./dist/result.html"

        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                template = f.read()
        else:
            template = default_template

        elapsed = round(time.time() - start_time, 1)
        html_content = template.replace("%SCRIPT_NAME%", script_name)\
            .replace("%TIME_TAKEN%", str(elapsed))\
            .replace("%SCRAPING_URL%", url)\
            .replace("%PLAYLIST_NAME%", playlist_title)\
            .replace("%DATA_LENGTH%", str(video_count))\
            .replace("%ALL_DATA%", "\n".join(html_snippets))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        webbrowser.open_new_tab(os.path.abspath(output_path))
        print_agent(f"{video_count} videos scraped and saved successfully.")

    except Exception as e:
        print_agent("An error occurred during scraping.")
        print(e)

    finally:
        driver.quit()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        os.makedirs("./logs", exist_ok=True)
        log_entry = f"[{timestamp}] {script_name} {url} length={video_count} time={elapsed}sec\n"
        with open("./logs/log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
        print_agent("Log saved to './logs/log.txt'")


if __name__ == "__main__":
    url = input("Enter the YouTube playlist URL: ").strip()
    scrape_playlist(url)
