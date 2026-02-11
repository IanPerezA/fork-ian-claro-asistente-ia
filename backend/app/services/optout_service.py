from datetime import datetime
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_default_database()

collection = db["opt_out_global"]

STOP_KEYWORDS = {"STOP", "CANCEL", "SALIR", "BAJA"}

def is_stop_command(message: str) -> bool:
    if not message:
        return False
    return message.strip().upper() in STOP_KEYWORDS


def mark_opt_out(phone_number: str):
    collection.update_one(
        {"phone_number": phone_number},
        {
            "$set": {
                "phone_number": phone_number,
                "opted_out_at": datetime.utcnow(),
            }
        },
        upsert=True
    )


def is_opted_out(phone_number: str) -> bool:
    return collection.find_one({"phone_number": phone_number}) is not None
