#!/usr/bin/env python3
"""
Generate product images for Brew Coffee Shop using Fal.ai API
"""

import requests
import json
import time
import os
from pathlib import Path

# Configuration
FAL_API_KEY = "f0e2b617-e22b-4960-a001-d6cd90677055:a29344d06654ce050ac52c6c2edc9841"
FAL_API_URL = "https://queue.fal.run/fal-ai/flux-pro"
IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Image prompts - detailed for high quality
PROMPTS = {
    # Coffee Beans - Iron Cans
    "coffee_beans_1.jpg": {
        "filename": "coffee_beans_1.jpg",
        "prompt": "Beautiful premium Ethiopian single origin coffee beans in a luxury brushed bronze metallic tin can with gold lid and elegant brown label, professional product photography on pure white background, studio lighting, high resolution, premium packaging",
        "product": "Ethiopian Highland"
    },
    "coffee_beans_2.jpg": {
        "filename": "coffee_beans_2.jpg",
        "prompt": "Luxury Colombian Geisha coffee beans in an elegant dark copper metallic tin with ornate details and rose gold lid, premium packaging, professional product shot on white background, studio lighting",
        "product": "Colombian Geisha"
    },
    "coffee_beans_3.jpg": {
        "filename": "coffee_beans_3.jpg",
        "prompt": "Premium Kenyan AA coffee beans in a shiny polished chrome silver metallic tin can with decorative lid and elegant label, luxury coffee product photography, white studio background, professional",
        "product": "Kenyan AA"
    },
    "coffee_beans_4.jpg": {
        "filename": "coffee_beans_4.jpg",
        "prompt": "Luxury coffee beans in a beautiful rose gold metallic tin with premium brushed finish and ornate lid, premium product photography, white studio background, professional shot",
        "product": "House Blend"
    },

    # Cricket Collaboration Tins
    "cricket_collab_green.jpg": {
        "filename": "cricket_collab_green.jpg",
        "prompt": "Premium coffee tin in deep forest green (IPL cricket team colors) with gold cricket bat and ball design embossed on side, golden metallic lid, luxury metallic finish, professional product photography on white background",
        "product": "Brew × Cricket Club - Green"
    },
    "cricket_collab_gold.jpg": {
        "filename": "cricket_collab_gold.jpg",
        "prompt": "Coffee tin in vibrant gleaming gold (IPL cricket team colors) with elegant cricket bat motif and green accents, premium metallic packaging, luxury finish, professional studio shot",
        "product": "Brew × Cricket Club - Gold"
    },
    "cricket_collab_red.jpg": {
        "filename": "cricket_collab_red.jpg",
        "prompt": "Coffee tin in bold deep red (cricket team colors) with gold cricket elements including bat and ball design, luxury metallic finish, premium packaging, professional product photography",
        "product": "Brew × Cricket Club - Red"
    },

    # Nespresso Capsules - GRIND Style
    "nespresso_1.jpg": {
        "filename": "nespresso_1.jpg",
        "prompt": "Nespresso compatible coffee pods box in warm pastel orange like GRIND brand, minimalist modern design with elegant typography, white background, professional product shot, luxury packaging",
        "product": "Espresso Ristretto"
    },
    "nespresso_2.jpg": {
        "filename": "nespresso_2.jpg",
        "prompt": "Premium coffee capsules box in soft pastel blue, modern minimalist eco-friendly aesthetic, clean elegant design like GRIND, professional product photography",
        "product": "Lungo Intenso"
    },
    "nespresso_3.jpg": {
        "filename": "nespresso_3.jpg",
        "prompt": "Nespresso pods box in gentle mint green pastel with elegant modern typography, sustainable coffee packaging design, professional product shot on white background",
        "product": "Harvest Colombia"
    },
    "nespresso_4.jpg": {
        "filename": "nespresso_4.jpg",
        "prompt": "Coffee capsules box in soft lavender pastel with gold accents and minimalist design, luxury eco-friendly packaging, professional product photography",
        "product": "Vanilla Decaffeinato"
    },

    # Iced Coffee - Aluminium Cans
    "iced_coffee_1.jpg": {
        "filename": "iced_coffee_1.jpg",
        "prompt": "Premium ready-to-drink cold brew coffee in sleek silver aluminium can 250ml with elegant logo, metallic finish, professional product photography on white studio background, luxury beverage packaging",
        "product": "Classic Cold Brew"
    },
    "iced_coffee_2.jpg": {
        "filename": "iced_coffee_2.jpg",
        "prompt": "Iced coffee in rich brown and gold metallic aluminium can 250ml, luxury beverage packaging, professional product shot, white background, studio lighting",
        "product": "Caramel Macchiato"
    },
    "iced_coffee_3.jpg": {
        "filename": "iced_coffee_3.jpg",
        "prompt": "Cold brew coffee in dark metallic black and gold aluminium can 250ml with coffee bean motif, premium packaging, professional studio photography",
        "product": "Espresso Black"
    },
    "iced_coffee_4.jpg": {
        "filename": "iced_coffee_4.jpg",
        "prompt": "Vanilla latte in soft cream and brown metallic aluminium can 250ml, luxury drink packaging, professional product photography on white background, studio lighting",
        "product": "Vanilla Latte"
    }
}

def submit_image_job(prompt):
    """Submit image generation job to Fal.ai and wait for completion"""
    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "num_images": 1,
        "image_size": "square_hd",
        "num_inference_steps": 30,
        "guidance_scale": 7.5
    }

    try:
        # Submit job
        response = requests.post(FAL_API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()

        # If we got a request_id, poll for completion
        if 'request_id' in result:
            request_id = result['request_id']
            poll_url = f"https://queue.fal.run/fal-ai/flux-pro/{request_id}/status"

            # Poll for up to 5 minutes
            for attempt in range(60):
                time.sleep(2)
                poll_response = requests.get(poll_url, headers=headers, timeout=30)
                poll_response.raise_for_status()
                status_result = poll_response.json()

                if status_result.get('status') == 'COMPLETED':
                    return status_result
                elif status_result.get('status') == 'FAILED':
                    print(f"⚠️  Job failed: {status_result.get('error', 'unknown')}")
                    return None

        return result
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None

def download_image(url, filepath):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Download Error: {e}")
        return False

def generate_all_images():
    """Generate all images for the coffee shop"""
    print("🎨 Brew Coffee Shop - Image Generation Started\n")
    print("=" * 60)

    total = len(PROMPTS)
    successful = 0
    failed = 0

    for idx, (filename, config) in enumerate(PROMPTS.items(), 1):
        print(f"\n[{idx}/{total}] Generating: {config['product']}")
        print(f"File: {filename}")
        print(f"Prompt: {config['prompt'][:70]}...")

        # Submit job
        result = submit_image_job(config['prompt'])

        if not result:
            print(f"⏳ Retrying...")
            time.sleep(2)
            result = submit_image_job(config['prompt'])

        if result and 'images' in result and len(result['images']) > 0:
            image_url = result['images'][0]['url']
            filepath = IMAGES_DIR / filename

            print(f"⏳ Downloading image...")
            if download_image(image_url, filepath):
                print(f"✅ Saved: {filepath}")
                successful += 1
            else:
                print(f"❌ Download failed")
                failed += 1
        else:
            print(f"⚠️  Generation status: {result.get('status', 'unknown') if result else 'no response'}")
            failed += 1

        # Rate limiting
        time.sleep(1)

    print("\n" + "=" * 60)
    print(f"\n📊 Results: {successful}/{total} successful, {failed} failed")
    return successful == total

if __name__ == "__main__":
    generate_all_images()
