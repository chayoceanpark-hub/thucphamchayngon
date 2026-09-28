import docx
import json
import os
import re

# Load images
image_files = [f for f in os.listdir('.') if f.endswith('.webp')]
images = {}
for img in image_files:
    match = re.match(r'^(\d+)\.\s*(.+)\.webp$', img)
    if match:
        images[int(match.group(1))] = {
            'image': img,
            'name': match.group(2).strip()
        }

# Read docx
doc = docx.Document('Thông tin sản phẩm chay.docx')
text_content = "\n".join([p.text for p in doc.paragraphs])

# Find all links
all_links = re.findall(r'https://s\.shopee\.vn/[a-zA-Z0-9]+', text_content)

products = []
for i in range(1, 65):
    if i in images:
        prod = {
            "id": i,
            "name": images[i]['name'],
            "image": images[i]['image'],
            "link": all_links[i-1] if i-1 < len(all_links) else "#"
        }
        products.append(prod)

with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("Saved products.json with 64 products.")
