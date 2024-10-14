from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def parse_scraped_data(scraped_data):
  prompt=    prompt = f"""
    You are a data parser. Your task is to extract useful information from the following data.

    Data:
    {scraped_data}

       
    """
  response = model.generate_content(prompt)
  print(response.text)