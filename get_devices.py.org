#!/usr/bin/env python3
import os, requests, json, sys

# --- Environment setup ---
API = os.getenv("NETBOX_API", "http://netbox-docker-netbox-1:8080").rstrip("/")
TOKEN = os.getenv("NETBOX_TOKEN", "").strip()
quiet = "--quiet" in sys.argv  # suppress debug output for Jenkins

# --- Validate environment variables ---
if not API or not TOKEN:
    print("❌ Missing NETBOX_API or NETBOX_TOKEN environment variables.")
    sys.exit(1)

# --- Build request ---
url = f"{API}/api/dcim/devices/?limit=0"
headers = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/json"
}

if not quiet:
    print(f"🔍 Fetching from: {url}")
    print(f"🔑 Using token prefix: {TOKEN[:6]}... (truncated)")

# --- Perform request ---
try:
    resp = requests.get(url, headers=headers, timeout=20)
except requests.exceptions.RequestException as e:
    print(f"❌ Connection error: {e}")
    sys.exit(1)

# --- Check HTTP status ---
if resp.status_code != 200:
    print(f"❌ HTTP {resp.status_code}: {resp.text[:300]}")
    sys.exit(1)

# --- Try parse JSON ---
try:
    data = resp.json()
except ValueError:
    print("❌ Invalid JSON response received from NetBox.")
    print("Response preview:")
    print(resp.text[:300])
    sys.exit(1)

# --- Extract device names ---
devices = [d.get("name") for d in data.get("results", []) if d.get("name")]

# --- Output ---
if quiet:
    print(json.dumps(devices))
else:
    print(f"✅ Found {len(devices)} devices:")
    print(json.dumps(devices, indent=2))
