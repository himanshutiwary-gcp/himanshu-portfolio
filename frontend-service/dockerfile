# 1. Use an official lightweight Python image.
FROM python:3.9-slim

# 2. Set environment variables
# - PYTHONUNBUFFERED: Ensures that print statements and logs are sent straight to the console (and Cloud Logging).
ENV PYTHONUNBUFFERED True

# 3. Set the working directory in the container
WORKDIR /app

# 4. Copy the dependencies file first to leverage Docker cache
# This step is only re-run if requirements.txt changes.
COPY requirements.txt .

# 5. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application's code into the container
# This includes app.py and the 'templates' and 'static' folders.
COPY . .

# 7. Define the command to run the application using a production-grade server (gunicorn)
# - Binds to the port provided by the Cloud Run environment variable $PORT
# - Disables Gunicorn's timeout to let Cloud Run manage request timeouts
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
