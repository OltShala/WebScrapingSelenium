from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# --------------------------------------
# SETUP CHROME DRIVER
# --------------------------------------
def setup_driver():
    options = Options()
    options.headless = False
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# --------------------------------------
# SCRAPE AMENITIES
# --------------------------------------
def scrape_amenities(driver):
    url = "https://www.hawthornvillageapts.com/apartments/ca/napa/amenities"
    driver.get(url)

    print("Scraping amenities...")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)

    amenities = []
    try:
        sections = driver.find_elements(By.CLASS_NAME, "column")
        for section in sections:
            items = section.find_elements(By.TAG_NAME, "li")
            for item in items:
                text = item.text.strip()
                if text:
                    amenities.append(text)
    except Exception as e:
        print(f"Could not scrape amenities: {e}")

    return amenities

# --------------------------------------
# SCRAPE FLOOR PLANS
# --------------------------------------
def scrape_apartments(driver, amenities_list):
    url = "https://www.hawthornvillageapts.com/apartments/ca/napa/floor-plans#/"
    driver.get(url)

    print("Waiting for floor plans to load...")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    try:
        view_all_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='View All Floor Plans']]"))
        )
        print("Clicking 'View All Floor Plans' button...")
        driver.execute_script("arguments[0].scrollIntoView(true);", view_all_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", view_all_btn)
        time.sleep(5)
    except TimeoutException:
        print("Could not find or click 'View All Floor Plans'. Proceeding anyway.")

    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.v-card.floorplan"))
    )
    listings = driver.find_elements(By.CSS_SELECTOR, "div.v-card.floorplan")
    print(f"Found {len(listings)} apartment listings.")

    data = []
    address = "3663 Solano Ave, Napa, CA 94558"

    for index, listing in enumerate(listings, start=1):
        print(f"Scraping listing {index}/{len(listings)}...")

        try:
            unit_name = listing.find_element(By.CSS_SELECTOR, "p.floorplan-title-title").text.strip()
        except NoSuchElementException:
            unit_name = "N/A"

        try:
            specs = listing.find_elements(By.CSS_SELECTOR, "p.floorplan-title-meta span")
            beds = specs[0].text.strip() if len(specs) > 0 else "N/A"
            baths = specs[1].text.strip() if len(specs) > 1 else "N/A"
            sqft = specs[2].text.strip() if len(specs) > 2 else "N/A"
        except:
            beds, baths, sqft = "N/A", "N/A", "N/A"

        try:
            price = listing.find_element(By.CSS_SELECTOR, "p.rate-display span.subheading").text.strip().replace('"', '')
        except NoSuchElementException:
            price = "N/A"

        try:
            availability = listing.find_element(By.CSS_SELECTOR, "p.availability").text.strip()
        except NoSuchElementException:
            availability = "Not specified"

        data.append({
            "Unit Name": unit_name,
            "Bedrooms": beds,
            "Bathrooms": baths,
            "Square Footage": sqft,
            "Price": price,
            "Availability": availability,
            "Address": address,
            "Amenities": ", ".join(amenities_list)
        })

    return data

# --------------------------------------
# SAVE DATA TO CSV
# --------------------------------------
def save_to_csv(data, filename="hawthorn_apartments.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"\n✅ Saved {len(data)} listings to '{filename}'\n")

# --------------------------------------
# MAIN EXECUTION
# --------------------------------------
if __name__ == "__main__":
    driver = setup_driver()
    try:
        amenities = scrape_amenities(driver)
        apartments = scrape_apartments(driver, amenities)
        if apartments:
            save_to_csv(apartments)
        else:
            print("No apartment data scraped.")
    finally:
        driver.quit()
