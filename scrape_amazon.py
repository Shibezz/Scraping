import os
import time
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from fake_useragent import UserAgent

# === Argument Parser ===
parser = argparse.ArgumentParser(description="Scrape Amazon product listings.")
parser.add_argument("--query", type=str, required=True, help="Search query (e.g., laptops, mobiles)")
parser.add_argument("--pages", type=int, default=10, help="Number of pages to scrape")
args = parser.parse_args()

query = args.query
pages = args.pages

# === Prepare output directory ===
base_dir = 'amazon_products'
output_dir = os.path.join(base_dir, query)

# Ensure base_dir is a directory, not a file
if os.path.exists(base_dir) and not os.path.isdir(base_dir):
    print(f" Error: {base_dir} exists and is not a directory.")
    exit(1)

# Make the output subdirectory
os.makedirs(output_dir, exist_ok=True)

# === Setup WebDriver ===
ua = UserAgent()
user_agent = ua.random

options = Options()
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Edge(options=options)

# === Scraping Logic ===
for pageNum in range(1, pages + 1):
    url = f"https://www.amazon.in/s?k={query}&page={pageNum}&ref=nb_sb_noss"
    print(f"Scraping page: {url}")
    try:
        driver.get(url)
        time.sleep(random.uniform(2.5, 5.0))  # Human-like delay

        products = driver.find_elements(By.CLASS_NAME, "puisg-row")
        print(f"Found {len(products)} products on page {pageNum}")

        for idx, product in enumerate(products, start=1):
            d = product.get_attribute('outerHTML')
            file_name = os.path.join(output_dir, f"product_{pageNum}_{idx}.html")
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(d)
    except Exception as e:
        print(f"Error on page {pageNum}: {e}")

# Final wait & close
time.sleep(4)
driver.quit()
