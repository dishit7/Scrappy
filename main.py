from scraper import scrape_website
from llm_integration import parse_scraped_data
def main():
    url = 'https://www.amazon.ca'  # Example URL
    scraped_data = scrape_website(url)
    
    print("Scraped Data:", scraped_data)
    parse_scraped_data(scraped_data)
if __name__ == "__main__":
    main()
