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
            time.sleep(6)

            # Flutter accessibility enable karo
            acc_btn = page.locator("flt-semantics-placeholder[aria-label='Enable accessibility']")
            if acc_btn.count() > 0:
                print("Enabling Flutter accessibility...")
                acc_btn.click()
                time.sleep(3)

            page.screenshot(path="after_load.png")

            # Ab flt-text-editing-host mein inputs aayenge jab field click karein
            # Flutter canvas pe Employee ID field ki position click karo
            # Login form center mein hai - Employee ID field click
            page.mouse.click(960, 258)  # Employee ID field position
            time.sleep(1)

            # Ab input DOM mein aayega
            emp_input = page.locator("flt-text-editing-host input, flt-semantics input").first
            emp_input.wait_for(state="attached", timeout=10000)
            emp_input.fill(USERNAME)
            print(f"Employee ID entered")

            # Password field click
            page.mouse.click(960, 292)
            time.sleep(1)
            pwd_input = page.locator("flt-text-editing-host input[type='password'], flt-semantics input[type='password']").first
            pwd_input.wait_for(state="attached", timeout=10000)
            pwd_input.fill(PASSWORD)
            print("Password entered")

            page.screenshot(path="before_login.png")

            # Login button click - canvas pe position
            page.mouse.click(960, 332)
            print("Login clicked")
            time.sleep(6)
            page.screenshot(path="after_login.png")

            if ACTION == "clockin":
                # Clock In button dhundo
                page.locator("flt-semantics[aria-label*='Clock In'], flt-semantics[role='button']").filter(has_text="Clock In").first.click()
                print("Clock In clicked!")
            elif ACTION == "clockout":
                page.locator("flt-semantics[aria-label*='Clock Out'], flt-semantics[role='button']").filter(has_text="Clock Out").first.click()
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
