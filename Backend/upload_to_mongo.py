import json
from pymongo import MongoClient

# MongoDB connection (change this if using MongoDB Atlas)
MONGO_URI = "mongodb://localhost:27017/"  # Local MongoDB
# MONGO_URI = "your_mongodb_atlas_connection_string"  # Use this for MongoDB Atlas

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["news_db"]  # Database name
collection = db["articles"]  # Collection name

# Load JSON file
with open("scraped_news.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Insert data into MongoDB
if isinstance(data, list):  # Ensure data is a list of documents
    collection.insert_many(data)
else:
    collection.insert_one(data)

print("Data uploaded successfully to MongoDB!")
