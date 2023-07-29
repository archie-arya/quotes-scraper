import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

# Replace <grid-hub-ip> with the actual IP address or hostname of your Selenium Grid hub.
# If running Selenium Grid on the same machine, you can use 'localhost' or '127.0.0.1'.
grid_url = "http://localhost:4444/wd/hub"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mcs_assignment']
collection = db['quotes']

# Define a function to scrape and store quotes from a single page
def scrape_page(page):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Remote(command_executor=grid_url, options=chrome_options)
    driver.get("http://quotes.toscrape.com/page/" + str(page + 1))

    for i in range(1, 11):
        quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
        author_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"

        quote_element = driver.find_element(By.XPATH, quote_xpath)
        quote_text = quote_element.text

        author_element = driver.find_element(By.XPATH, author_xpath)
        author_name = author_element.text

        print("Quote:", quote_text)
        print("Author:", author_name)
        print()

        document = {
            'quote_id': page * 10 + i,
            'quote': quote_text,
            'author': author_name
        }
        collection.insert_one(document)

    driver.quit()

# Scrape quotes from 10 pages concurrently using multiple threads
threads = []
for page in range(10):
    thread = threading.Thread(target=scrape_page, args=(page,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("Scraping completed!!")
