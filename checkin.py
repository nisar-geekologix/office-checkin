import os
import sys
import requests

USERNAME = os.environ["OFFICE_USERNAME"]
PASSWORD = os.environ["OFFICE_PASSWORD"]
ACTION   = os.environ.get("ACTION", "clockin")

BASE = "https://api.taskyz.com/api2/v1"

# Step 1: Login
login_res = requests.post(f"{BASE}/login", json={
    "login_type": "employee_cred",
    "employee_id": USERNAME,
    "password": PASSWORD,
    "device_type": "web",
    "device_id": "web-browser",
    "fcmToken": ""
})

login_data = login_res.json()
if login_data.get("status") != 1:
    print(f"Login failed: {login_data}")
    sys.exit(1)

token = login_data["data"]["token"]
print(f"Login successful: {login_data['message']}")

headers = {"Authorization": f"Bearer {token}"}

# Step 2: Clock In ya Clock Out
if ACTION == "clockin":
    res = requests.get(f"{BASE}/checkin", headers=headers)
elif ACTION == "clockout":
    res = requests.get(f"{BASE}/checkout", headers=headers)

data = res.json()
print(f"Result: {data['message']}")

if data.get("status") != 1:
    print("Action failed!")
    sys.exit(1)
