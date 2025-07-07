from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os 
 
try:
     MONGO_URI = os.getenv('MONGO_URI')
    # Replace with your URI if using MongoDB Atlas
     client = MongoClient(MONGO_URI)
     db = client['action-repo1']
     events_collection = db['github-events']
     client.server_info() 
     print("✅ MongoDB connection successful!")

except ConnectionFailure as e:
    print(" MongoDB connection failed:", e)

