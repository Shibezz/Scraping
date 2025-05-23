from bs4 import BeautifulSoup
import os
import json

folder_path = "./amazon_products/"
output_json = './amazon_products.json'

# Keywords that likely indicate a laptop product
laptop_keywords = [
    "laptop", "notebook", "intel", "amd", "dell", "hp", "asus", "lenovo", 
    "acer", "macbook", "chromebook", "15-inch", "14-inch", "13-inch", "gaming"
]

exclude_keywords = [
    "bag", "cover", "sleeve", "mouse", "keyboard", "adapter", "charger", "case", "stand", "tablet"
]

def is_laptop(title):
    if not title:
        return False
    title_lower = title.lower()
    
    # Exclude if any exclude keywords present
    if any(ex_kw in title_lower for ex_kw in exclude_keywords):
        return False
    
    # Include if any laptop keywords present
    return any(kw in title_lower for kw in laptop_keywords)


products = []

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.stat(file_path).st_size == 0:
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    title = soup.find('h2').get_text(strip=True) if soup.find('h2') else None

    # Filter only laptops
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

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print(f"Filtered JSON file saved: {output_json}")
