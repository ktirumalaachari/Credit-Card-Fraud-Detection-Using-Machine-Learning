from flask import Blueprint, request, jsonify
from auth.email_service import send_email
from werkzeug.security import generate_password_hash, check_password_hash
from auth.models import *
from auth.utils import *

auth_bp = Blueprint("auth", __name__)

# SIGNUP
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json

    if find_user(data["email"]):
        return {"msg": "User exists"}, 400

    otp = generate_otp()
    save_otp(data["email"], otp)

    send_email(data["email"], "OTP Verification", f"Your OTP is {otp}")
    print("OTP:", otp)

    create_user({
        "email": data["email"],
        "password": generate_password_hash(data["password"]),
        "verified": False
    })

    return {"msg": "OTP generated ( check your email )"}

# VERIFY OTP
@auth_bp.route("/verify", methods=["POST"])
def verify():
    data = request.json

    record = verify_otp(data["email"], data["otp"])

    if not record:
        return {"msg": "Invalid OTP"}, 400

    update_user(data["email"], {"verified": True})

    return {"msg": "Email verified"}


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = find_user(data["email"])

    if not user:
        return {"msg": "User not found"}, 404

    if not user.get("verified"):
        return {"msg": "Please verify email"}, 401

    if check_password_hash(user["password"], data["password"]):
        token = generate_token(data["email"])
        return {"token": token}

    return {"msg": "Wrong password"}, 401


# FORGOT PASSWORD
@auth_bp.route("/forgot", methods=["POST"])
def forgot():
    data = request.json

    if not find_user(data["email"]):
        return {"msg": "User not found"}, 404

    otp = generate_otp()
    save_otp(data["email"], otp)

    send_email(data["email"], "OTP Verification", f"Your OTP is {otp}")
    print("OTP:", otp)

    return {"msg": "OTP generated (check terminal)"}


# RESET PASSWORD
@auth_bp.route("/reset", methods=["POST"])
def reset():
    data = request.json

    if not verify_otp(data["email"], data["otp"]):
        return {"msg": "Invalid OTP"}, 400

    hashed = generate_password_hash(data["password"])
    update_user(data["email"], {"password": hashed})

    return {"msg": "Password updated"}