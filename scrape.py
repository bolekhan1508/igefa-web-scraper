from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

# Initialize the WebDriver
driver = webdriver.Chrome()

# Define the file path for the intermediate dataset
csv_file_path = 'scraped_products.csv'


# Check if the file exists. If not, create it and add headers.
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Product Name", "Breadcrumb", "Ausführung", "Supplier Article Number",
            "EAN/GTIN", "Article Number", "Product Description", "Supplier",
            "Supplier-URL", "Product Image URL", "Manufacturer", "Additional Description"
        ])

# Function to save product data to CSV
def save_to_csv(product_info):
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            product_info.get("Product Name"), product_info.get("Breadcrumb"),
            product_info.get("Ausführung"), product_info.get("Supplier Article Number"),
            product_info.get("EAN/GTIN"), product_info.get("Article Number"),
            product_info.get("Product Description"), product_info.get("Supplier"),
            product_info.get("Supplier-URL"), product_info.get("Product Image URL"),
            product_info.get("Manufacturer"), product_info.get("Additional Description")
        ])

# Function to get saved product count to know where to resume
def get_saved_product_count():
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        return sum(1 for row in file) - 1  # Subtract header row

try:
    # Open the target website
    driver.get('https://store.igefa.de/')

    # Wait for the cookie consent button and click it
    cookie_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'))
    )
    cookie_button.click()

    # Get the number of saved products to resume scraping
    saved_count = get_saved_product_count()

    # Function to get product links
    def get_product_links():
        # Wait for the product elements to load
        product_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[data-testid="productCard_productName"]'))
        )
        return [
            product_element.find_element(By.XPATH, './ancestor::div[contains(@class, "ant-card")]')
            for product_element in product_elements
        ]

    # Extract product links initially
    product_links = get_product_links()
    print(f"Found {len(product_links)} products.")

    # Loop through products starting from the last saved index
    for index in range(saved_count, len(product_links)):
        try:
            # Scroll to the product link
            driver.execute_script("arguments[0].scrollIntoView();", product_links[index])
            time.sleep(1)

            # Click on the product link
            product_links[index].click()

            # Wait for the product detail page to load
            product_detail_title = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pdp-product-info-product-name"]'))
            )

            # Extract product details with error handling for optional elements
            product_info = {"Product Name": product_detail_title.text}

            try:
                breadcrumb_link = driver.find_element(By.CSS_SELECTOR, 'div.CategoryBreadcrumbs_breadcrumbWrap__fa56d:nth-child(4) a')
                product_info["Breadcrumb"] = breadcrumb_link.get_attribute("href")
            except:
                product_info["Breadcrumb"] = None

            try:
                product_info["Ausführung"] = driver.find_element(By.XPATH, '//*[@id="__next"]/section/main/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]').text.split(": ")[1]
            except:
                product_info["Ausführung"] = None

            try:
                product_info["Supplier Article Number"] = driver.find_element(By.XPATH, '//div[@data-testid="product-information-sku"]').text.split(": ")[1]
            except:
                product_info["Supplier Article Number"] = None

            try:
                product_info["EAN/GTIN"] = driver.find_element(By.XPATH, '//div[@data-testid="product-information-gtin"]').text.split(": ")[1]
            except:
                product_info["EAN/GTIN"] = None

            try:
                product_info["Article Number"] = driver.find_element(By.XPATH, '//span[@data-testid="product-number"]').text
            except:
                product_info["Article Number"] = None

            try:
                product_info["Product Description"] = driver.find_element(By.XPATH, '//div[@data-testid="product-description"]').text
            except:
                product_info["Product Description"] = None

            product_info["Supplier"] = "igefa Handelsgesellschaft"
            product_info["Supplier-URL"] = driver.current_url

            try:
                product_info["Product Image URL"] = driver.find_element(By.CSS_SELECTOR, 'img[class="image-gallery-image"]').get_attribute('src')
            except:
                product_info["Product Image URL"] = None

            try:
                manufacturer_row = driver.find_element(By.XPATH, '//tr[td[text()="Hersteller"]]/td[2]')
                product_info["Manufacturer"] = manufacturer_row.text
            except:
                product_info["Manufacturer"] = None

            try:
                product_info["Additional Description"] = driver.find_element(By.XPATH, '//div[@class="ProductBenefits_productBenefits__1b77a"]').text
            except:
                product_info["Additional Description"] = None

            # Print and save product details
            print(f'Product {index + 1}: {product_info}')
            save_to_csv(product_info)
            print('---')

        except Exception as e:
            print(f'Could not retrieve details for product {index + 1}: {e}')
            if 'stale element reference' in str(e).lower():
                product_links = get_product_links()

        # Go back to the main page and re-extract product links
        driver.back()
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[data-testid="productCard_productName"]'))
        )
        product_links = get_product_links()

except Exception as e:
    print(f'An error occurred: {e}')

finally:
    driver.quit()
