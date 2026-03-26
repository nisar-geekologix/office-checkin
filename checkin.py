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

            # Flutter accessibility enable - force click (element is hidden at -1,-1)
            page.evaluate("""
                const btn = document.querySelector("flt-semantics-placeholder");
                if (btn) { btn.click(); console.log('accessibility clicked'); }
            """)
            print("Accessibility enabled via JS")
            time.sleep(4)
            page.screenshot(path="after_accessibility.png")

            # Ab page pe Tab key se focus karo aur type karo
            # Ya directly canvas coordinates pe click karo
            # Employee ID field - screenshot mein ~y=258 tha
            page.mouse.click(512, 258)
            time.sleep(1)
            page.keyboard.type(USERNAME)
            print(f"Employee ID typed: {USERNAME}")

            # Password field
            page.mouse.click(512, 292)
            time.sleep(1)
            page.keyboard.type(PASSWORD)
            print("Password typed")

            page.screenshot(path="before_login.png")

            # Login button ~y=332
            page.mouse.click(512, 332)
            print("Login clicked")
            time.sleep(6)
            page.screenshot(path="after_login.png")

            # Clock In/Out button
            if ACTION == "clockin":
                # Dashboard pe Clock In button position
                page.mouse.click(452, 108)
                print("Clock In clicked!")
            elif ACTION == "clockout":
                page.mouse.click(452, 108)
                print("Clock Out clicked!")

            time.sleep(3)
            page.screenshot(path=f"{ACTION}_done.png")
            print(f"{ACTION} done!")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path=f"{ACTION}_error.png")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
