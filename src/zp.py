import argparse
import time
import csv
import os
import re
from datetime import datetime
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def setup_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--width=1200")
    options.add_argument("--height=800")
    options.add_argument("--headless")  # For background execution
    return webdriver.Firefox(options=options)


def login_to_zwiftpower(driver, email, password):
    driver.get("https://zwiftpower.com/")
    time.sleep(2)

    login_button = driver.find_element(By.LINK_TEXT, "Login with Zwift")
    login_button.click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    WebDriverWait(driver, 30).until(EC.url_contains("zwiftpower.com"))


def scrape_profile_data(driver, profile_url):
    driver.get(profile_url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'zFTP')]"))
    )

    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "weight": None,
        "zftp": None,
        "15s_w": None, "1m_w": None, "5m_w": None, "20m_w": None,
        "15s_wkg": None, "1m_wkg": None, "5m_wkg": None, "20m_wkg": None,
    }

    try:
        rows = driver.find_elements(By.XPATH, "//tr[th and td]")
        for row in rows:
            label = row.find_element(By.XPATH, "./th").text.strip().lower()
            value = row.find_element(By.XPATH, "./td").text.strip()

            if "zftp" in label:
                data["zftp"] = value
            elif "weight" in label:
                data["weight"] = value

        source = driver.page_source
        watts = extract_power(source, "w")
        wkg = extract_power(source, "wkg")

        for k in ["15s", "1m", "5m", "20m"]:
            data[f"{k}_w"] = watts.get(k)
            data[f"{k}_wkg"] = wkg.get(k)

        return data

    except Exception as e:
        print("Error extracting data:", e)
        return data


def extract_power(source, category: str):
    matches = re.findall(r"<b>(15 seconds|1 minute|5 minutes|20 minutes)</b>: ([\d\.]+)\s*<rsmall>" + category, source)
    power_dict = {}
    for label, power in matches:
        if label.startswith("15"):
            power_dict["15s"] = power
        elif label.startswith("1 "):
            power_dict["1m"] = power
        elif label.startswith("5"):
            power_dict["5m"] = power
        elif label.startswith("20"):
            power_dict["20m"] = power
    return power_dict


def write_to_csv(filepath, data):
    header = [
        "date", "weight", "zftp",
        "15s_w", "1m_w", "5m_w", "20m_w",
        "15s_wkg", "1m_wkg", "5m_wkg", "20m_wkg"
    ]

    file_exists = os.path.isfile(filepath)

    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)

        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def main():
    parser = argparse.ArgumentParser(description="ZwiftPower Scraper with CSV logging and formatted output")
    parser.add_argument("--email", required=True, help="Zwift account email")
    parser.add_argument("--password", required=True, help="Zwift account password")
    parser.add_argument("--url", required=True, help="ZwiftPower profile URL")
    parser.add_argument("--csv", required=True, help="Path to CSV output file")

    args = parser.parse_args()

    driver = setup_driver()

    try:
        login_to_zwiftpower(driver, args.email, args.password)
        data = scrape_profile_data(driver, args.url)
        write_to_csv(args.csv, data)
        print(f"\n✅ Data written to {args.csv}\n")
        print("📊 Scraped Profile Data:")
        pprint(data, sort_dicts=False)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
