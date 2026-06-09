#!/usr/bin/env python3
"""
Fetch generated images from Fal.ai using the API
"""

import requests
import json
from pathlib import Path

FAL_API_KEY = "f0e2b617-e22b-4960-a001-d6cd90677055:a29344d06654ce050ac52c6c2edc9841"
IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

headers = {
    "Authorization": f"Key {FAL_API_KEY}",
    "Content-Type": "application/json"
}

# Try to get recent requests/results from Fal.ai
print("🔍 Fetching Fal.ai account info and recent generations...")

try:
    # Get user info
    user_response = requests.get("https://api.fal.ai/v1/user", headers=headers, timeout=30)
    user_response.raise_for_status()
    user_info = user_response.json()
    print(f"✅ Connected to Fal.ai account")
    print(f"Account: {json.dumps(user_info, indent=2)}")
except Exception as e:
    print(f"⚠️ Could not fetch user info: {e}")

# Try to list recent requests
print("\n🔍 Checking for recent image generation requests...")

try:
    # This endpoint might list recent requests
    requests_response = requests.get(
        "https://api.fal.ai/v1/requests",
        headers=headers,
        timeout=30
    )
    requests_response.raise_for_status()
    requests_data = requests_response.json()
    print(f"Recent requests: {json.dumps(requests_data, indent=2)}")
except Exception as e:
    print(f"⚠️ Could not fetch requests list: {e}")

print("\n📋 Next step: Check Fal.ai dashboard at https://fal.ai to see generated images")
