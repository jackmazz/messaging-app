from pymongo import MongoClient
import os
import uuid

def create_record(collection, record):
    record_id = str(uuid.uuid4())
    record.setdefault("id", record_id)
    collection.insert_one(record)
    return record_id

def delete_record(collection, query):
    collection.delete_one(query)

def list_records(collection):
    return list(collection.find({}, {"_id": False}))

def retrieve_record(collection, query):
    return collection.find_one(query, {"_id": False})

def update_record(collection, query, record):
    collection.update_one(query, {"$set": record})

docker_debug = os.environ.get('DOCKER_DEBUG', "false")
client = None
if docker_debug == "true":
    print("Using mongo_debug database")
    client = MongoClient("mongo_debug")
else:
    print("Using mongo database")
    client = MongoClient("mongo")
database = client["cse312"]
accounts = database["accounts"]
posts = database["posts"]