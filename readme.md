# Twitter Trends Scraper with Flask and MongoDB

This application scrapes trending topics from Twitter using Selenium and proxies, stores them in a MongoDB database, and provides a simple Flask-based web interface to run the scraper.

## Features

- **Scrapes Twitter trends**: The application scrapes the top trending topics from Twitter using Selenium WebDriver.
- **Proxy support**: The scraper uses a proxy server to scrape data while masking the IP address.
- **Flask Web Interface**: A simple Flask-based API that allows you to trigger the scraper and view the results.
- **MongoDB Storage**: The scraped trending topics are stored in a MongoDB database with timestamps and proxy IP addresses.

## Prerequisites

Before running the app, make sure you have the following installed:

- Python 3.x
- MongoDB running locally or remotely
- Chrome WebDriver (`chromedriver.exe`) in the same directory as the script (or specify its path)
- Flask
- Selenium
- Requests
- python-dotenv

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Prince29chouhan/Twitter_top_trending.git
   cd <your-repository-folder>
   ```

2. **Create a virtual environment (optional but recommended):**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

   ```

3. **Install the required Python packages:**:

   ```bash
   pip install -r requirements.txt

   ```

4. **Set up the .env file:**:
   Create a .env file in the root directory and add your credentials and MongoDB configuration:

   ```bash
   TWITTER_USERNAME=YourTwitterUsername
   TWITTER_PASSWORD=YourTwitterPassword
   PROXY_USERNAME=YourProxyUsername
   PROXY_PASSWORD=YourProxyPassword
   PROXY_IP=YourProxyIP
   PROXY_PORT=YourProxyPort
   MONGO_URI=mongodb://localhost:27017
   DATABASE_NAME=stir_tech
   COLLECTION_NAME=trending_topics

   ```

5. **Run the Flask app:**:

   ```bash
    python app.py

   ```

**Ensure MongoDB is running:**

If you're running MongoDB locally, ensure it's up and running.
If using a cloud database, update the MONGO_URI in the .env file.

**Example response:**

```bash
   {
  "_id": "generated-uuid",
  "trend1": "Trending Topic 1",
  "trend2": "Trending Topic 2",
  "trend3": "Trending Topic 3",
  "trend4": "Trending Topic 4",
  "trend5": "Trending Topic 5",
  "timestamp": "2024-12-26T00:00:00",
  "ip_address": "YourProxyIP"
}


```
