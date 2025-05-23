import os
import json
import argparse
from bs4 import BeautifulSoup

# === Parse Arguments ===
parser = argparse.ArgumentParser(description="Extract product info from scraped HTML files.")
parser.add_argument("--query", type=str, required=True, help="Query folder inside amazon_products/ (e.g., laptops, mobiles)")
args = parser.parse_args()

folder_path = os.path.join("amazon_products", args.query)
output_json = f'./{args.query}_products.json'

# Keywords for identifying laptop-like items
laptop_keywords = [
    "laptop", "notebook", "intel", "amd", "dell", "hp", "asus", "lenovo", 
    "acer", "macbook", "chromebook", "15-inch", "14-inch", "13-inch", "gaming"
]

exclude_keywords = [
    "bag", "cover", "sleeve", "mouse", "keyboard", "adapter", "charger", 
    "case", "stand", "tablet", "toy"
]

def is_laptop(title):
    if not title:
        return False
    title_lower = title.lower()
    if any(ex_kw in title_lower for ex_kw in exclude_keywords):
        return False
    return any(kw in title_lower for kw in laptop_keywords)

# === Extract Product Info ===
products = []

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.path.isdir(file_path):
        continue  #  Skip subfolders

    if os.stat(file_path).st_size == 0:
        continue  #  Skip empty files

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    title = soup.find('h2').get_text(strip=True) if soup.find('h2') else None

    if not is_laptop(title):
        continue

    price = soup.find('span', {'class': 'a-price-whole'}).get_text(strip=True) if soup.find('span', {'class': 'a-price-whole'}) else None
    url = (
        'https://www.amazon.in' + soup.find('div', {'data-cy': 'title-recipe'}).find('a')['href']
        if soup.find('div', {'data-cy': 'title-recipe'}) and soup.find('div', {'data-cy': 'title-recipe'}).find('a')
        else None
    )
    img_url = soup.find('img')['src'] if soup.find('img') else None
    rating = soup.find('span', class_='a-icon-alt').get_text(strip=True) if soup.find('span', class_='a-icon-alt') else None

    if not all([title, price, url, img_url, rating]):
        continue

    product = {
        "title": title,
        "price": price,
        "product_link": url,
        "image_link": img_url,
        "rating": rating
    }
    products.append(product)

# === Save Output ===
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print(f" Filtered JSON file saved to: {output_json}")
