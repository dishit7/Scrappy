# app.py
from flask import Flask
from  app.routes.scrape_route import scrape_blueprint  # Directly import the blueprint
from app.routes.query_route import query_blueprint
app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(scrape_blueprint, url_prefix="/api")
app.register_blueprint(query_blueprint, url_prefix="/api")


@app.route("/")
def home():
    return "Welcome to the API!"

if __name__ == "__main__":
    app.run(debug=True)
