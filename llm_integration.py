from dotenv import load_dotenv
import google.generativeai as genai
import os
from pinecone import Pinecone



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
pinecone_api_key=os.environ.get("PINECONE_API_KEY")


 
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("scrappy")

print(pinecone_api_key)
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
 
 
def parse_scraped_data(scraped_data):
    prompt = f"""
    Parse and summarize the following scraped web content:

    {scraped_data}

    Instructions:
    1. Remove irrelevant information, ads, and boilerplate text.
    2. Organize content into coherent paragraphs or sections.
    3. Preserve key facts, figures, and important quotes.
    4. Maintain original meaning and context.
    5. Use clear and concise language.
    6. Include relevant headings or subheadings.
    7. Ensure each paragraph can stand alone for embedding.
    8. Extract and include the title and meta description if available.
    9. Add a brief summary at the beginning.

    Format the output as:
    Title: [Extracted title]
    Summary: [Brief overview]
    Content:
    [Organized and parsed content]
    """
    response = model.generate_content(prompt)
    parsed_content = response.text
    print(parsed_content)
 
     


    