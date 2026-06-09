#!/usr/bin/env python3
"""
Generate and download images from Fal.ai using correct API
"""

import requests
import json
import time
from pathlib import Path

FAL_API_KEY = "f0e2b617-e22b-4960-a001-d6cd90677055:a29344d06654ce050ac52c6c2edc9841"
IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Correct Fal.ai endpoint for async queue
SUBMIT_URL = "https://queue.fal.run/fal-ai/flux-pro"

prompts = {
    "coffee_beans_1.jpg": "Beautiful premium Ethiopian single origin coffee beans in a luxury brushed bronze metallic tin can with gold lid and elegant brown label, professional product photography on pure white background, studio lighting, high resolution, premium packaging",
    "coffee_beans_2.jpg": "Luxury Colombian Geisha coffee beans in an elegant dark copper metallic tin with ornate details and rose gold lid, premium packaging, professional product shot on white background, studio lighting",
    "coffee_beans_3.jpg": "Premium Kenyan AA coffee beans in a shiny polished chrome silver metallic tin can with decorative lid and elegant label, luxury coffee product photography, white studio background, professional",
    "coffee_beans_4.jpg": "Luxury coffee beans in a beautiful rose gold metallic tin with premium brushed finish and ornate lid, premium product photography, white studio background, professional shot",
    "cricket_collab_green.jpg": "Premium coffee tin in deep forest green (IPL cricket team colors) with gold cricket bat and ball design embossed on side, golden metallic lid, luxury metallic finish, professional product photography on white background",
    "cricket_collab_gold.jpg": "Coffee tin in vibrant gleaming gold (IPL cricket team colors) with elegant cricket bat motif and green accents, premium metallic packaging, luxury finish, professional studio shot",
    "cricket_collab_red.jpg": "Coffee tin in bold deep red (cricket team colors) with gold cricket elements including bat and ball design, luxury metallic finish, premium packaging, professional product photography",
    "nespresso_1.jpg": "Nespresso compatible coffee pods box in warm pastel orange like GRIND brand, minimalist modern design with elegant typography, white background, professional product shot, luxury packaging",
    "nespresso_2.jpg": "Premium coffee capsules box in soft pastel blue, modern minimalist eco-friendly aesthetic, clean elegant design like GRIND, professional product photography",
    "nespresso_3.jpg": "Nespresso pods box in gentle mint green pastel with elegant modern typography, sustainable coffee packaging design, professional product shot on white background",
    "nespresso_4.jpg": "Coffee capsules box in soft lavender pastel with gold accents and minimalist design, luxury eco-friendly packaging, professional product photography",
    "iced_coffee_1.jpg": "Premium ready-to-drink cold brew coffee in sleek silver aluminium can 250ml with elegant logo, metallic finish, professional product photography on white studio background, luxury beverage packaging",
    "iced_coffee_2.jpg": "Iced coffee in rich brown and gold metallic aluminium can 250ml, luxury beverage packaging, professional product shot, white background, studio lighting",
    "iced_coffee_3.jpg": "Cold brew coffee in dark metallic black and gold aluminium can 250ml with coffee bean motif, premium packaging, professional studio photography",
    "iced_coffee_4.jpg": "Vanilla latte in soft cream and brown metallic aluminium can 250ml, luxury drink packaging, professional product photography on white background, studio lighting",
}

def submit_job(prompt):
    """Submit image generation job"""
    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "num_images": 1,
        "image_size": "square_hd",
        "num_inference_steps": 50,
        "guidance_scale": 7.5
    }
    
    try:
        response = requests.post(SUBMIT_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  ❌ Submit error: {e}")
        return None

print("🎨 Brew Coffee Shop - Fal.ai Image Generation\n")
print("=" * 60)

total = len(prompts)
successful = 0
failed = 0

for idx, (filename, prompt) in enumerate(prompts.items(), 1):
    print(f"\n[{idx}/{total}] {filename}")
    print(f"Submitting to Fal.ai...")
    
    result = submit_job(prompt)
    
    if result:
        request_id = result.get('request_id')
        status = result.get('status')
        print(f"  Request ID: {request_id}")
        print(f"  Status: {status}")
        
        if request_id:
            print(f"  Check status at: https://fal.ai/dashboard")
            successful += 1
        else:
            failed += 1
    else:
        failed += 1
    
    time.sleep(0.5)

print("\n" + "=" * 60)
print(f"\n📊 Submitted: {successful}/{total} jobs")
print(f"\n📋 Next step: Go to https://fal.ai/dashboard")
print(f"   Download all generated images and run: python3 manual_download.py")
