#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Image specifications
products = [
    # Coffee Beans
    ("coffee_beans_1.jpg", "#8B4513", "Ethiopian\nHighland"),
    ("coffee_beans_2.jpg", "#6B3410", "Colombian\nGeisha"),
    ("coffee_beans_3.jpg", "#704214", "Kenyan AA"),
    ("coffee_beans_4.jpg", "#9D6B3D", "House Blend"),
    # Cricket Collaboration
    ("cricket_collab_green.jpg", "#1a472a", "Cricket\nGreen"),
    ("cricket_collab_gold.jpg", "#ffd700", "Cricket\nGold"),
    ("cricket_collab_red.jpg", "#c41e3a", "Cricket\nRed"),
    # Nespresso Capsules
    ("nespresso_1.jpg", "#FF6B35", "Espresso\nRistretto"),
    ("nespresso_2.jpg", "#2E86C1", "Lungo\nIntenso"),
    ("nespresso_3.jpg", "#27AE60", "Harvest\nColombia"),
    ("nespresso_4.jpg", "#8E44AD", "Vanilla\nDecaff"),
    # Iced Coffee
    ("iced_coffee_1.jpg", "#C0C0C0", "Cold Brew"),
    ("iced_coffee_2.jpg", "#A9927D", "Caramel\nMacchiato"),
    ("iced_coffee_3.jpg", "#6F4E37", "Espresso\nBlack"),
    ("iced_coffee_4.jpg", "#D4A574", "Vanilla\nLatte"),
]

for filename, color, label in products:
    img = Image.new('RGB', (300, 300), color=color)
    draw = ImageDraw.Draw(img)
    
    # Add border
    draw.rectangle([5, 5, 295, 295], outline='white', width=3)
    
    # Add text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Center text
    text_bbox = draw.textbbox((0, 0), label, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (300 - text_width) // 2
    y = (300 - text_height) // 2
    
    draw.text((x, y), label, fill='white', font=font)
    
    filepath = IMAGES_DIR / filename
    img.save(filepath)
    print(f"✅ Created: {filename}")

print(f"\n✨ All {len(products)} images created in {IMAGES_DIR}")
