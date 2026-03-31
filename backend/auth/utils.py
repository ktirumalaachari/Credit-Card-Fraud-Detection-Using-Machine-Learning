import jwt
import datetime
import random

SECRET = "fraud_detection_jwt_secret_nist_2026"

def generate_token(email):
    return jwt.encode({
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET, algorithm="HS256")

def generate_otp():
    return str(random.randint(100000, 999999))