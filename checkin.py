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

            # Flutter app ko fully load hone do
            print("Waiting for Flutter to render...")
            time.sleep(8)
            page.screenshot(path="after_load.png")

            # Flutter renders everything in a <canvas> or flt-* elements
            # Check what's actually in the DOM
            body_html = page.inner_html("body")
            print("Body snippet:", body_html[:2000])

            # Flutter web uses flt-semantics for accessibility
            # Wait for flutter semantic elements
            page.wait_for_selector("flt-semantics-container", timeout=20000)
            print("Flutter rendered!")
            page.screenshot(path="flutter_loaded.png")

            # Flutter inputs are inside flt-semantics
            inputs = page.locator("input")
            print(f"Input count: {inputs.count()}")

            # Fill first input (Employee ID)
            inputs.nth(0).click()
            inputs.nth(0).fill(USERNAME)
            print("Employee ID entered")

            # Fill second input (Password)
            inputs.nth(1).click()
            inputs.nth(1).fill(PASSWORD)
            print("Password entered")

            page.screenshot(path="before_login.png")

            # Click Login - Flutter button
            page.locator("flt-semantics[role='button']", has_text="Login").click()
            print("Login clicked")
            time.sleep(5)
            page.screenshot(path="after_login.png")

            if ACTION == "clockin":
                page.locator("flt-semantics[role='button']", has_text="Clock In").click()
                print("Clock In clicked!")
            elif ACTION == "clockout":
                page.locator("flt-semantics[role='button']", has_text="Clock Out").click()
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
