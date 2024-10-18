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
 

def generate_embedding(content):
    max_length = 9000

    content_chunks = []
    while len(content) > max_length:
        split_index = content.rfind(' ', 0, max_length)
        if split_index == -1:
            split_index = max_length
        content_chunks.append(content[:split_index])
        content = content[split_index:].strip()
    
    if content:
        content_chunks.append(content)

    for i, chunk in enumerate(content_chunks):
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=chunk,
            task_type="retrieval_document",
            title=f"Embedding of chunk {i + 1}"
        )

        embedding = result['embedding']
        
        # Include the content in the metadata
        metadata = {
            "title": f"Chunk {i + 1}",
            "source": "scraped_website",
            "content": chunk  # Add this line
        }

        index.upsert([(f"doc-{i+1}", embedding, metadata)])

        print(f"Upserted embedding for chunk {i + 1}: {str(embedding)[:50]} ... TRIMMED")


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
    generate_embedding(parsed_content)

  
     


