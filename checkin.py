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
            page.goto(URL, timeout=60000)
            time.sleep(3)  # JS render hone do
            page.screenshot(path="after_load.png")

            # Employee ID - placeholder text se dhundo
            emp = page.locator("input").nth(0)
            emp.wait_for(state="visible", timeout=15000)
            emp.click()
            emp.fill(USERNAME)
            print(f"Employee ID entered: {USERNAME}")

            # Password - second input
            pwd = page.locator("input").nth(1)
            pwd.click()
            pwd.fill(PASSWORD)
            print("Password entered")

            page.screenshot(path="before_login.png")

            # Login button
            page.locator("button", has_text="Login").click()
            print("Login clicked, waiting...")
            time.sleep(5)
            page.screenshot(path="after_login.png")

            if ACTION == "clockin":
                page.locator("button", has_text="Clock In").wait_for(state="visible", timeout=15000)
                page.locator("button", has_text="Clock In").click()
                print("Clock In clicked!")

            elif ACTION == "clockout":
                page.locator("button", has_text="Clock Out").wait_for(state="visible", timeout=15000)
                page.locator("button", has_text="Clock Out").click()
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
