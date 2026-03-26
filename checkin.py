import os
import sys
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

USERNAME = os.environ["OFFICE_USERNAME"]
PASSWORD = os.environ["OFFICE_PASSWORD"]
ACTION   = os.environ.get("ACTION", "clockin")
URL      = "https://taskyz.com/web/minified:u4"

def get_chromedriver_path():
    # chromedriver jo system mein installed hai uska path dhundo
    result = subprocess.run(["which", "chromedriver"], capture_output=True, text=True)
    path = result.stdout.strip()
    if path:
        print(f"Found chromedriver at: {path}")
        return path
    return "/usr/bin/chromedriver"

def run():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(executable_path=get_chromedriver_path())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"Opening: {URL}")
        driver.get(URL)
        wait = WebDriverWait(driver, 20)

        # Employee ID
        emp_field = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@placeholder='Employee ID' or @type='text']"
        )))
        emp_field.clear()
        emp_field.send_keys(USERNAME)
        print("Employee ID entered")

        # Password
        pwd_field = driver.find_element(By.XPATH, "//input[@type='password']")
        pwd_field.clear()
        pwd_field.send_keys(PASSWORD)
        print("Password entered")

        # Login
        login_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Login')]")
        login_btn.click()
        print("Login clicked, waiting...")
        time.sleep(4)

        if ACTION == "clockin":
            btn = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(text(),'Clock In')]"
            )))
            btn.click()
            print("Clock In successful!")

        elif ACTION == "clockout":
            btn = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(text(),'Clock Out')]"
            )))
            btn.click()
            print("Clock Out successful!")

        time.sleep(3)
        driver.save_screenshot(f"{ACTION}_success.png")

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot(f"{ACTION}_error.png")
        sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    run()
