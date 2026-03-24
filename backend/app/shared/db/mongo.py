from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class MongoConnection:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["whatsapp_db"]

    def get_collection(self, name: str):
        return self.db[name]

mongo = MongoConnection()