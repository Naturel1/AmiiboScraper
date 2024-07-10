from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time


def setup_driver():
    # Config for the Firefox browser
    options = Options()
    options.headless = False  # Open the browser window if False

    # Geckodriver path
    geckodriver_path = './geckodriver'

    # Create the firefox instance
    service = Service(geckodriver_path)

    # Init the firefox driver with the specified options and service
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def scrape_amiibo_info():
    driver = setup_driver()
    try:
        # Open the amiibo page
        driver.get('https://store.nintendo.be/fr/games/enhance-your-play-games/amiibo')

        # Wait for the page to load
        time.sleep(5)

        # Close the cookie banner if present
        try:
            cookie_banner = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
            cookie_banner.click()
            time.sleep(2)
        except Exception as e:
            print("No cookie banner found or unable to close it.")

        # scroll down to the amiibo filter
        filter = driver.find_element(By.ID, 'orderable_only0')
        driver.execute_script("arguments[0].scrollIntoView();", filter)
        time.sleep(1)

        # Activate the filter by disponibility
        driver.execute_script("arguments[0].click();", filter)

        time.sleep(5)

        # Locate the amiibo container on the page
        amiibo_container = driver.find_element(By.CSS_SELECTOR, ".row.product-grid")

        # Extend the page until every element are visible
        amiibo_items = amiibo_container.find_elements(By.XPATH, './*')
        while amiibo_items[-1].get_attribute('class') == "col-12 grid-footer":
            driver.execute_script("arguments[0].scrollIntoView();", amiibo_items[-1])
            time.sleep(1)
            amiibo_items[-1].click()
            time.sleep(3)
            amiibo_items = amiibo_container.find_elements(By.XPATH, './*')

        # Print and save every amiibo in the page
        for item in amiibo_items:
            text = item.text
            lines = text.split('\n')
            if len(lines) >= 3:
                combined_line = lines[-3] + " - " + lines[-2]
                print(combined_line)
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the driver when done
        driver.quit()


if __name__ == "__main__":
    scrape_amiibo_info()
