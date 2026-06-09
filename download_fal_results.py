#!/usr/bin/env python3
"""
Download images from Fal.ai using request IDs
"""

import requests
import json
from pathlib import Path

FAL_API_KEY = "f0e2b617-e22b-4960-a001-d6cd90677055:a29344d06654ce050ac52c6c2edc9841"
IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Request IDs from previous generations
request_ids = {
    "coffee_beans_1.jpg": "019eae79-b358-7173-8ff5-8b562446f21f",
    "coffee_beans_2.jpg": "019eae79-dddc-7212-b252-24f3fe468293",
    "coffee_beans_3.jpg": "019eae7a-020f-7bf0-8c66-f120cb16e54c",
    "coffee_beans_4.jpg": "019eae7a-2620-7cd3-9cda-ff4b0506b2fb",
    "cricket_collab_green.jpg": "019eae7a-4a23-74e3-a7b4-f85a187560bc",
    "cricket_collab_gold.jpg": "019eae7a-6e20-7872-99e2-044f46cad122",
    "cricket_collab_red.jpg": "019eae7a-915f-7ac1-ada8-ac74c2708911",
    "nespresso_1.jpg": "019eae7a-b4e1-7bc2-b477-18478561d4b2",
    "nespresso_2.jpg": "019eae7a-d8b6-7653-aa36-5eff9a107c0a",
    "nespresso_3.jpg": "019eae7a-fc37-70d3-97cb-61b0c3281e3a",
    "nespresso_4.jpg": "019eae7b-20c5-7ec2-909d-7061d74cf0f9",
    "iced_coffee_1.jpg": "019eae7b-4799-7861-aacb-e3c6b8625297",
    "iced_coffee_2.jpg": "019eae7b-6d00-7250-81c1-4a43c4247af0",
    "iced_coffee_3.jpg": "019eae7b-92c3-7ed1-bcc1-9209df4fa61a",
    "iced_coffee_4.jpg": "019eae7b-b690-7153-b910-80e8198b276d",
}

headers = {
    "Authorization": f"Key {FAL_API_KEY}",
}

print("🔍 Checking Fal.ai queue results...")

for filename, request_id in request_ids.items():
    url = f"https://queue.fal.run/fal-ai/flux-pro/{request_id}/status"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        status_data = response.json()
        
        print(f"\n📦 {filename}")
        print(f"   Status: {status_data.get('status', 'unknown')}")
        
        if 'result' in status_data:
            result = status_data['result']
            if 'images' in result and len(result['images']) > 0:
                img_url = result['images'][0]['url']
                print(f"   URL: {img_url}")
                
                # Try to download
                try:
                    img_response = requests.get(img_url, timeout=30)
                    img_response.raise_for_status()
                    filepath = IMAGES_DIR / filename
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    print(f"   ✅ Downloaded to {filepath}")
                except Exception as e:
                    print(f"   ❌ Download failed: {e}")
        else:
            print(f"   Data: {json.dumps(status_data, indent=2)}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n✨ Done!")
