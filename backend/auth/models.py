from auth.db import users, otps

def create_user(data):
    users.insert_one(data)

def find_user(email):
    return users.find_one({"email": email})

def update_user(email, data):
    users.update_one({"email": email}, {"$set": data})

import datetime
def save_otp(email, otp):
    otps.delete_many({"email": email})  #Remove old OTPs
    otps.insert_one({
        "email": email,
        "otp": otp,
        "expires_at": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    })

def verify_otp(email, otp):
    record = otps.find_one({"email": email, "otp": otp})
    if record:
        otps.delete_one({"email": email})  # Delete after use
    return record