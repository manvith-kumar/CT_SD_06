from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Setup Chrome driver (make sure to download the appropriate chromedriver and add it to PATH)
driver = webdriver.Chrome()

def scrape_myntra_with_selenium(url, max_pages=1):
    products = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        driver.get(f"{url}?p={page}")
        time.sleep(5)  # wait for JavaScript to load

        product_cards = driver.find_elements(By.CLASS_NAME, 'product-base')

        for card in product_cards:
            try:
                name = card.find_element(By.CLASS_NAME, 'product-brand').text + " " + \
                       card.find_element(By.CLASS_NAME, 'product-product').text
                try:
                    price = card.find_element(By.CLASS_NAME, 'product-discountedPrice').text
                except:
                    price = card.find_element(By.CLASS_NAME, 'product-price').text
                try:
                    original_price = card.find_element(By.CLASS_NAME, 'product-strike').text
                except:
                    original_price = 'N/A'
                try:
                    discount = card.find_element(By.CLASS_NAME, 'product-discountPercentage').text
                except:
                    discount = 'N/A'
                link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

                products.append({
                    'name': name,
                    'price': price,
                    'original_price': original_price,
                    'discount': discount,
                    'url': link
                })
            except Exception as e:
                print(f"Error: {e}")
                continue

    driver.quit()
    return pd.DataFrame(products)

# Example usage
url = input("Enter Myntra product listing URL: ")
max_pages = int(input("Enter number of pages: "))
df = scrape_myntra_with_selenium(url, max_pages)
df.to_csv("myntra_products.csv", index=False)
print("✅ Scraping done!")
