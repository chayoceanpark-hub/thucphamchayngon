import os
import re
import json

# 1. Map IDs to image filenames
image_files = [f for f in os.listdir('.') if f.endswith('.webp')]
id_to_image = {}
for img in image_files:
    match = re.match(r'^(\d+)\.', img)
    if match:
        id_to_image[int(match.group(1))] = img

# 2. Parse output.txt
with open('output.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

products = []
current_product = None

for line in lines:
    line = line.strip()
    if not line.startswith('PARAGRAPH:'):
        continue
    
    text = line.replace('PARAGRAPH:', '', 1).strip()
    
    # Check if this line is the start of a new product
    # Example: "1. Nước chấm muối tắc chai 250ml https://s.shopee.vn/8V9HPa45Th"
    match = re.match(r'^(\d+)\.\s+(.+?)\s+(https?://\S+)', text)
    if match:
        # Save previous product
        if current_product:
            products.append(current_product)
        
        prod_id = int(match.group(1))
        name = match.group(2).strip()
        link = match.group(3).strip()
        
        current_product = {
            'id': prod_id,
            'name': name,
            'link': link,
            'image': id_to_image.get(prod_id, ''),
            'description': ''
        }
    else:
        # Accumulate description
        if current_product and text:
            # Avoid adding empty descriptions or just "MÔ TẢ SẢN PHẨM" over and over
            if text.lower() not in ['mô tả sản phẩm', 'mô tả sản phẩm:']:
                current_product['description'] += text + '\n'

# Add the last product
if current_product:
    products.append(current_product)

# Clean up descriptions
for p in products:
    p['description'] = p['description'].strip()

# Sort by ID
products.sort(key=lambda x: x['id'])

# 3. Write to data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print(f"Successfully extracted {len(products)} products to data.json")
