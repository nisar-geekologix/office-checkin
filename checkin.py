import os
import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

USERNAME = os.environ["OFFICE_USERNAME"]
PASSWORD = os.environ["OFFICE_PASSWORD"]
ACTION   = os.environ.get("ACTION", "clockin")
URL      = "https://taskyz.com/web/minified:u4"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            print(f"Opening: {URL}")
            page.goto(URL, wait_until="networkidle")
            page.screenshot(path="after_load.png")

            # Employee ID
            page.fill("input[placeholder='Employee ID']", USERNAME)
            print("Employee ID entered")

            # Password
            page.fill("input[type='password']", PASSWORD)
            print("Password entered")

            # Login
            page.click("button:has-text('Login')")
            print("Login clicked, waiting...")
            page.wait_for_load_state("networkidle")
            time.sleep(3)
            page.screenshot(path="after_login.png")

            if ACTION == "clockin":
                page.click("button:has-text('Clock In')")
                print("Clock In clicked!")
            elif ACTION == "clockout":
                page.click("button:has-text('Clock Out')")
                print("Clock Out clicked!")

            time.sleep(3)
            page.screenshot(path=f"{ACTION}_success.png")
            print(f"{ACTION} successful!")

        except PlaywrightTimeout as e:
            print(f"Timeout Error: {e}")
            page.screenshot(path=f"{ACTION}_error.png")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path=f"{ACTION}_error.png")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
