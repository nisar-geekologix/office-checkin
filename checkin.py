import os
import sys
import time
from playwright.sync_api import sync_playwright

USERNAME = os.environ["OFFICE_USERNAME"]
PASSWORD = os.environ["OFFICE_PASSWORD"]
ACTION   = os.environ.get("ACTION", "clockin")
URL      = "https://taskyz.com/web/minified:u4"

def wait_and_print_dom(page, label):
    time.sleep(2)
    page.screenshot(path=f"{label}.png")
    # flt-semantics elements print karo
    elements = page.evaluate("""
        () => {
            const els = document.querySelectorAll('flt-semantics[role="button"], flt-semantics[role="textbox"]');
            return Array.from(els).map(e => ({
                role: e.getAttribute('role'),
                label: e.getAttribute('aria-label'),
                text: e.textContent.trim().substring(0, 50)
            }));
        }
    """)
    print(f"[{label}] flt-semantics elements:", elements)
    return elements

def click_flutter_button(page, label_text):
    result = page.evaluate(f"""
        () => {{
            const els = document.querySelectorAll('flt-semantics');
            for (const el of els) {{
                const label = el.getAttribute('aria-label') || el.textContent || '';
                if (label.toLowerCase().includes('{label_text.lower()}')) {{
                    el.click();
                    return 'clicked: ' + label;
                }}
            }}
            return 'not found: {label_text}';
        }}
    """)
    print(f"Button click result: {result}")
    return result

def type_in_flutter_input(page, index, text):
    # Flutter input fields ko focus karke type karo
    result = page.evaluate(f"""
        () => {{
            const inputs = document.querySelectorAll('flt-semantics[role="textbox"]');
            if (inputs[{index}]) {{
                inputs[{index}].focus();
                inputs[{index}].click();
                return 'focused input ' + {index};
            }}
            return 'input {index} not found, total: ' + inputs.length;
        }}
    """)
    print(f"Input focus result: {result}")
    time.sleep(0.5)
    page.keyboard.type(text)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            print(f"Opening: {URL}")
            page.goto(URL, timeout=60000)
            time.sleep(6)

            # Accessibility enable
            page.evaluate("""
                const btn = document.querySelector('flt-semantics-placeholder');
                if (btn) btn.click();
            """)
            time.sleep(4)

            els = wait_and_print_dom(page, "after_accessibility")

            # Employee ID input
            type_in_flutter_input(page, 0, USERNAME)
            print(f"Employee ID typed")
            time.sleep(0.5)

            # Password input
            type_in_flutter_input(page, 1, PASSWORD)
            print(f"Password typed")
            time.sleep(0.5)

            page.screenshot(path="before_login.png")

            # Login button click
            result = click_flutter_button(page, "login")
            print(f"Login: {result}")
            time.sleep(6)

            wait_and_print_dom(page, "after_login")

            # Clock In / Clock Out
            if ACTION == "clockin":
                result = click_flutter_button(page, "clock in")
                print(f"Clock In: {result}")
            elif ACTION == "clockout":
                result = click_flutter_button(page, "clock out")
                print(f"Clock Out: {result}")

            time.sleep(3)
            page.screenshot(path=f"{ACTION}_final.png")
            print("Done!")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path=f"{ACTION}_error.png")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
