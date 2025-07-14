import os
from flask import Flask, redirect
from google.cloud import storage

app = Flask(__name__)
storage_client = storage.Client()
BUCKET_NAME = os.environ.get("BUCKET_NAME")

@app.route("/images/<image_name>")
def serve_image(image_name):
    """
    Generates a signed URL to provide temporary access to a private GCS object.
    This is a secure way to serve images without making the bucket public.
    """
    if not BUCKET_NAME:
        return "Bucket name not configured", 500

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(image_name)

    if not blob.exists():
        return "Image not found", 404

    # Generate a signed URL valid for 10 minutes
    signed_url = blob.generate_signed_url(version="v4", expiration=600)

    return redirect(signed_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))