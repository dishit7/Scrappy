from scraper import scrape_website
from llm_integration import parse_scraped_data,generate_query_embedding,llm_query_response,search_similar_content
 
def process_user_query(user_query):
     
    query_embedding = generate_query_embedding(user_query)
    context = search_similar_content(query_embedding)
    response = llm_query_response(user_query, context)

    return response 
def main():
    url = 'https://www.gadgets360.com/news'  # Example URL
    scraped_data = scrape_website(url)
    
    print("Scraped Data:", scraped_data)
    parse_scraped_data(scraped_data)
    query="what is the latest sports news related to india currently" 
    output=process_user_query(query)
    print(output)
    
if __name__ == "__main__":
    main()
