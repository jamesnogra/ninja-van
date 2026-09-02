import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import the email function from send_mail.py
from send_mail import send_tracking_email

FILE_NAME = "tracking_log.txt"
tracking_id = "YWNUL454630527YP"
url = f"https://www.ninjavan.co/en-ph/international/tracking?id={tracking_id}"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=900,900")
chrome_options.add_argument("--disable-gpu")
# Required flags for running Chrome inside Linux/Ubuntu server as root
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

try:
    print(f"Opening URL: {url}")
    driver.get(url)

    print("Waiting for all list of updates to load...")
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'ant-timeline-item-content')]")
        )
    )

    all_list = driver.find_elements(
        By.XPATH, "//div[contains(@class, 'ant-timeline-item-content')]/div"
    )

    latest_status = all_list[0].text.strip()
    latest_timestamp = all_list[1].text.strip()
    formatted_entry = f"{latest_status} | {latest_timestamp}"

    # 1. Read the last saved line if file exists
    last_entry = ""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
            if lines:
                last_entry = lines[-1].strip()

    # 2. Append and send email only if it is different
    if formatted_entry != last_entry:
        with open(FILE_NAME, "a") as f:
            f.write(formatted_entry + "\n")
        print(f"New update saved: {formatted_entry}")

        # Send email via send_mail.py
        send_tracking_email(latest_status, latest_timestamp, tracking_id)
    else:
        print("No new updates found.")

finally:
    driver.quit()