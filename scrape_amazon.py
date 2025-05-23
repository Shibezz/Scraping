import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from fake_useragent import UserAgent

# === Setup ===

# Load proxies from proxy.txt
# with open('proxy.txt') as f:
#     proxy_list = [line.strip() for line in f if line.strip()]

# # Pick a random proxy
# proxy = random.choice(proxy_list)

# Generate a random user-agent
ua = UserAgent()
user_agent = ua.random

# Configure Edge options
options = Options()
#options.add_argument(f'--proxy-server=http://{proxy}')
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Start Edge
driver = webdriver.Edge(options=options)

# === Scraping Logic ===

query = 'laptops'
pages = 10
output_dir = 'amazon_products'
os.makedirs(output_dir, exist_ok=True)

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
