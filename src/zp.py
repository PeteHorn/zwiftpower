import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def setup_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--width=1200")
    options.add_argument("--height=800")
    return webdriver.Firefox(options=options)



def login_to_zwiftpower(driver, email, password):
    driver.get("https://zwiftpower.com/")
    time.sleep(2)
    
    login_button = driver.find_element(By.LINK_TEXT, "Login with Zwift")
    login_button.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    driver.find_element(By.NAME, "username").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    WebDriverWait(driver, 30).until(
        EC.url_contains("zwiftpower.com")
    )

def scrape_profile_data(driver, profile_url):
    driver.get(profile_url)

    # Wait until zFTP appears (ensures full profile is loaded)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'zFTP')]"))
    )

    data = {
        "zftp": None,
        "weight": None,
        "power": {
            "15s": None,
            "1m": None,
            "5m": None,
            "20m": None
        },
        "power_wkg": {
            "15s": None,
            "1m": None,
            "5m": None,
            "20m": None
        }
    }

    try:
        # Extract zFTP and Weight from the table
        rows = driver.find_elements(By.XPATH, "//tr[th and td]")
        for row in rows:
            label = row.find_element(By.XPATH, "./th").text.strip().lower()
            value = row.find_element(By.XPATH, "./td").text.strip()

            if "zftp" in label:
                data["zftp"] = value
            elif "weight" in label:
                data["weight"] = value

        # Load page source for regex parsing
        source = driver.page_source

        # Extract watts
        watts_matches = re.findall(r"<b>(15 seconds|1 minute|5 minutes|20 minutes)</b>: (\d+)\s*<rsmall>w", source)
        for label, watts in watts_matches:
            if label.startswith("15"):
                data["power"]["15s"] = f"{watts}w"
            elif label.startswith("1 "):
                data["power"]["1m"] = f"{watts}w"
            elif label.startswith("5"):
                data["power"]["5m"] = f"{watts}w"
            elif label.startswith("20"):
                data["power"]["20m"] = f"{watts}w"

        # Extract w/kg
        wkg_matches = re.findall(r"<b>(15 seconds|1 minute|5 minutes|20 minutes)</b>: ([\d\.]+)\s*<rsmall>wkg", source)
        for label, wkg in wkg_matches:
            if label.startswith("15"):
                data["power_wkg"]["15s"] = f"{wkg}wkg"
            elif label.startswith("1 "):
                data["power_wkg"]["1m"] = f"{wkg}wkg"
            elif label.startswith("5"):
                data["power_wkg"]["5m"] = f"{wkg}wkg"
            elif label.startswith("20"):
                data["power_wkg"]["20m"] = f"{wkg}wkg"

        return data

    except Exception as e:
        print("Error extracting data:", e)
        return data



def main():
    parser = argparse.ArgumentParser(description="ZwiftPower Scraper using Selenium")
    parser.add_argument("--email", required=True, help="Zwift account email")
    parser.add_argument("--password", required=True, help="Zwift account password")
    parser.add_argument("--url", default="https://zwiftpower.com/profile.php?z=123456",
                        help="ZwiftPower profile or race URL")

    args = parser.parse_args()

    driver = setup_driver()

    try:
        login_to_zwiftpower(driver, args.email, args.password)
        print(scrape_profile_data(driver, args.url))
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
