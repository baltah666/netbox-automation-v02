#!/usr/bin/env python3
import os, requests, json, sys

API = os.getenv("NETBOX_API", "http://netbox-docker-netbox-1:8080/api/")
TOKEN = os.getenv("NETBOX_TOKEN")
quiet = "--quiet" in sys.argv  # if Jenkins passes this flag, suppress debug

headers = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/json"
}

url = f"{API}dcim/devices/?limit=0"

if not quiet:
    print(f"🔍 Fetching: {url}")
    print(f"🔑 Using token: {TOKEN[:6]}... (truncated)")

resp = requests.get(url, headers=headers)
resp.raise_for_status()

data = resp.json()
devices = [d["name"] for d in data["results"] if d["name"]]

# Print only JSON if quiet
if quiet:
    print(json.dumps(devices))
else:
    print(json.dumps(devices, indent=2))
