from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def initialize_driver():
    # Setting up Chrome with required options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Headless mode for running without opening the browser window
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the Chrome driver using WebDriver Manager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver



def scrape_website(url, title_selector, content_selector):
    driver = initialize_driver()
    driver.get(url)  # Load the website

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extract title and content based on the CSS selectors
    title = soup.select_one(title_selector).get_text(strip=True) if soup.select_one(title_selector) else 'No title found'
    content = soup.select_one(content_selector).get_text(strip=True) if soup.select_one(content_selector) else 'No content found'
    
    driver.quit()  # Close the driver when done
    
    return {
        'title': title,
        'content': content
    }

