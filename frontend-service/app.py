import os
import requests
from flask import Flask, render_template, abort

app = Flask(__name__)

PROJECTS_API_URL = os.environ.get("PROJECTS_API_URL")
IMAGE_SERVICE_URL = os.environ.get("IMAGE_SERVICE_URL")

@app.route("/")
def home():
    if not PROJECTS_API_URL or not IMAGE_SERVICE_URL:
        # If config is missing, return an error.
        abort(500, description="Application is not configured correctly.")

    try:
        # Fetch project data from the projects API
        response = requests.get(f"{PROJECTS_API_URL}/api/projects")
        response.raise_for_status() # Raises an HTTPError for bad responses
        projects = response.json()
    except requests.exceptions.RequestException as e:
        # Handle cases where the API is down or returns an error
        print(f"Error fetching projects: {e}")
        projects = []
        
    return render_template("index.html", projects=projects, image_service_url=IMAGE_SERVICE_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))