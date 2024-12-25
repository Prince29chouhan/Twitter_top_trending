import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
from datetime import datetime
import uuid
import requests
from flask import Flask, jsonify, render_template
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from .env file
load_dotenv()

# Twitter Credentials
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

# Proxy Configuration
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")
PROXY_IP = os.getenv("PROXY_IP")
PROXY_PORT = os.getenv("PROXY_PORT")
proxy_url = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_IP}:{PROXY_PORT}"

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Flask App
app = Flask(__name__)

def get_proxy_ip(proxy_url):
    try:
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)
        proxy_ip = response.json().get("ip")
        return proxy_ip
    except Exception as e:
        print(f"Error fetching proxy IP: {e}")
        return None


def scrape_twitter_trends():
    chrome_options = webdriver.ChromeOptions()

    # Proxy configuration
    chrome_options.add_argument(f"--proxy-server={proxy_url}")
    
    service = Service(executable_path="chromedriver.exe", options=chrome_options)
    driver = webdriver.Chrome(service=service)

    try:
        # Get the actual IP address assigned by the proxy
        ip_address = get_proxy_ip(proxy_url)

        # Navigate to Twitter login
        driver.get("https://twitter.com/login")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
        )

        # Log in
        username_field = driver.find_element(By.XPATH, "//input[@name='text']")
        username_field.send_keys(TWITTER_USERNAME)
        next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        next_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        password_field = driver.find_element(By.XPATH, "//input[@name='password']")
        password_field.send_keys(TWITTER_PASSWORD)
        login_button = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
        login_button.click()

        # Wait until the "Show more" button is visible
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@href='/explore/tabs/for-you' and contains(@class, 'css-175oi2r')]//span[contains(text(), 'Show more')]")
            )
        )

        show_more_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@dir='ltr' and contains(@class, 'css-1jxf684')]"))
        )

        # Scrape trending topics
        trends_elements = driver.find_elements(By.XPATH, "//span[@dir='ltr' and contains(@class, 'css-1jxf684')]")
        trending_topics = [trend.text for trend in trends_elements if trend.text.strip()]

        # Create Record
        record = {
            "_id": str(uuid.uuid4()),
            "trend1": trending_topics[0] if len(trending_topics) > 0 else None,
            "trend2": trending_topics[1] if len(trending_topics) > 1 else None,
            "trend3": trending_topics[2] if len(trending_topics) > 2 else None,
            "trend4": trending_topics[3] if len(trending_topics) > 3 else None,
            "trend5": trending_topics[4] if len(trending_topics) > 4 else None,
            "timestamp": datetime.now(),
            "ip_address": ip_address  # Save actual proxy IP address
        }

        # Store Record in MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        collection.insert_one(record)
        client.close()

        return record

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        driver.quit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-script", methods=["POST"])
def run_script():
    result = scrape_twitter_trends()
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to scrape Twitter trends"}), 500

if __name__ == "__main__":
    app.run(debug=True)
