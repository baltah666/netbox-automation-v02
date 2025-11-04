#!/usr/bin/env python3
import os, requests, json

API = os.getenv("NETBOX_API", "http://netbox-docker-netbox-1:8080/api/")
TOKEN = os.getenv("NETBOX_TOKEN")  # ✅ this line fixed

headers = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/json"
}

url = f"{API}dcim/devices/?limit=0"
print(f"🔍 Fetching: {url}")
print(f"🔑 Using token: {TOKEN[:6]}... (truncated)")

resp = requests.get(url, headers=headers)
print(f"Status code: {resp.status_code}")

# Print preview of response body
print("Response preview:\n", resp.text[:500])

# Try to parse JSON safely
try:
    data = resp.json()
    devices = [d["name"] for d in data["results"]]
    print(json.dumps(devices, indent=2))
except Exception as e:
    print("⚠️ Could not parse JSON:", e)
