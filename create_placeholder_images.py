from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(text, filename, size=(400, 400), bg_color=(200, 200, 200), text_color=(100, 100, 100)):
    """Create a placeholder image with text"""
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a basic font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Get text bounding box
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center the text
    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)
    draw.text(position, text, fill=text_color, font=font)
    
    # Save the image
    img.save(filename)
    print(f"Created: {filename}")

# Create category placeholder images
categories = [
    'Chair', 'Sofa', 'Table', 'Wardrobe', 'Bed', 
    'Cabinet', 'Shelf', 'Armchair', 'Outdoor'
]

for category in categories:
    filename = os.path.join('media', 'categories', f'{category.lower()}.jpg')
    create_placeholder_image(category, filename, size=(600, 400))

# Create product placeholder images
products = [
    'modern-office-chair', 'ergonomic-desk-chair', 'dining-chair-set',
    'l-shaped-sectional-sofa', '3-seater-leather-sofa', 'modern-loveseat',
    'glass-dining-table', 'wooden-coffee-table', 'standing-desk',
    '3-door-wardrobe', 'sliding-door-wardrobe', 'walk-in-closet',
    'king-size-bed', 'queen-storage-bed', 'twin-bunk-bed',
    'bedside-table', 'storage-cabinet', 'nightstand',
    '5-tier-bookshelf', 'floating-shelf', 'industrial-shelf',
    'leather-recliner', 'accent-armchair', 'wingback-chair',
    'patio-dining-set', 'garden-lounge-chair', 'outdoor-sofa'
]

for i, product in enumerate(products, 1):
    filename = os.path.join('media', 'products', f'{product}.jpg')
    create_placeholder_image(f'Product {i}', filename, size=(800, 800))

print("\nAll placeholder images created successfully!")