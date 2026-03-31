from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["fraud_detection"]

users = db["users"]
otps = db["otps"]