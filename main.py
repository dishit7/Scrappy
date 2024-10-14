from scraper import scrape_website
 
def main():
    url = 'https://www.amazon.in/gp/bestsellers'  # Example URL
    scraped_data = scrape_website(url)
    
     
    print("Scraped Data:", scraped_data)
 
if __name__ == "__main__":
    main()
