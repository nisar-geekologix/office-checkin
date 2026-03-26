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
print(f"Login: {login_data['message']}")

headers = {
    "Authorization": f"Bearer {token}",
    "Origin": "https://taskyz.com",
    "Referer": "https://taskyz.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

# Step 2: Organization fetch
org_res = requests.get(f"{BASE}/organizations", headers=headers)
org_data = org_res.json()
org_id = org_data["data"][0]["id"]
user_role = org_data["data"][0]["user_role"]
print(f"Org: {org_id}, Role: {user_role}")

headers["org-id"] = org_id
headers["user-role"] = user_role

# Step 3: Clock In ya Clock Out
if ACTION == "clockin":
    res = requests.get(f"{BASE}/checkin", headers=headers)
elif ACTION == "clockout":
    res = requests.get(f"{BASE}/checkout", headers=headers)

data = res.json()
print(f"Result: {data['message']}")

if data.get("status") != 1:
    print("Action failed!")
    sys.exit(1)
