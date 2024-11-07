# scrape_route.py
import datetime
from bson import ObjectId
from flask import Blueprint, jsonify, request
from app.services.scraper import scrape_website
from app.db.models import ScrapedContent
from app.services.llm_integration import parse_scraped_data

# Create a Blueprint
scrape_blueprint = Blueprint("scrape", __name__)

@scrape_blueprint.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    url = data.get("url")
    user_id = data.get("user_id")

    if not url:
        return jsonify({"error": "URL is required"}), 400
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        scraped_data = scrape_website(url)
        scraped_content = scraped_data.get("body_content")
        summary = parse_scraped_data(scraped_content)

        scraped_content_data = {
            "user_id": ObjectId(user_id),
            "url": url,
            "content": scraped_content,
            "summary": summary,
            "created_at": datetime.datetime.now()
        }

        ScrapedContent.save_scraped_content(scraped_content_data)

        result = {
            "scraped_data": scraped_content,
            "summary": summary
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
