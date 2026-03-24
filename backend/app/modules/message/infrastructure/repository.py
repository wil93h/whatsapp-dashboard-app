from app.shared.db.mongo import mongo
from datetime import datetime

class MessageRepository:

    def __init__(self):
        self.collection = mongo.get_collection("messages")

    def create(self, texto: str, numero: str):
        result = self.collection.insert_one({
            "texto": texto,
            "numero": numero,
            "timestamp": datetime.utcnow(),
            "status": "processing"
        })
        return result.inserted_id

    def update_analysis(self, message_id, data: dict):
        self.collection.update_one(
            {"_id": message_id},
            {
                "$set": {
                    "sentimiento": data["sentimiento"],
                    "tema": data["tema"],
                    "resumen": data["resumen"],
                    "status": "processed"
                }
            }
        )

    def get_sentiments(self):
        pipeline = [
            {"$group": {"_id": "$sentimiento", "count": {"$sum": 1}}}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_themes(self):
        pipeline = [
            {"$group": {"_id": "$tema", "count": {"$sum": 1}}}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_recent(self):
        return list(self.collection.find().sort("timestamp", -1).limit(10))