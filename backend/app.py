from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import numpy as np
import pickle
import pandas as pd
import os
import warnings
import jwt
from functools import wraps

# AUTH IMPORT
from auth.auth_routes import auth_bp

warnings.filterwarnings("ignore", category=UserWarning)

# PATH CONFIG
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../frontend/templates"),
    static_folder=os.path.join(BASE_DIR, "../frontend/static")
)

app.secret_key = "fraud_detection_secret"

# REGISTER AUTH ROUTES
app.register_blueprint(auth_bp, url_prefix="/auth")

# ===================== LOAD MODELS =====================

def load_model(filename):
    path = os.path.join(BASE_DIR, "models", filename)
    with open(path, "rb") as f:
        return pickle.load(f)

rf_model = load_model("random_forest_model.pkl")
xgb_model = load_model("xgboost_model.pkl")
lgb_model = load_model("lightgbm_model.pkl")
cat_model = load_model("catboost_model.pkl")
hybrid_cfg = load_model("hybrid_thresholds.pkl")

# ===================== TOKEN SECURITY =====================

SECRET = "fraud_detection_jwt_secret_nist_2026"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"msg": "Token missing"}), 401

        try:
            jwt.decode(token, SECRET, algorithms=["HS256"])
        except:
            return jsonify({"msg": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

# ===================== ROUTES =====================

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


# DISABLED OLD LOGIN
@app.route('/do_login', methods=['POST'])
def do_login():
    return jsonify({"msg": "Use /auth/login API"})


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/visualizations.html')
def visualizations():
    return render_template('visualizations.html')


@app.route('/analysis.html')
def analysis():
    return render_template('analysis.html')


@app.route('/amount-trends.html')
def amount_trends():
    return render_template('amount-trends.html')


@app.route('/feature.html')
def feature():
    return render_template('feature.html')


@app.route('/theory.html')
def theory():
    return render_template('theory.html')


@app.route('/model.html')
def model():
    return render_template('model.html')


@app.route('/privacy-policy.html')
def privacy_policy():
    return render_template('privacy-policy.html')


@app.route('/terms-conditions.html')
def terms_conditions():
    return render_template('terms-conditions.html')

@app.route('/verify')
def verify_page():
    return render_template('verify.html')


@app.route('/forgot')
def forgot_page():
    return render_template('forgot.html')


@app.route('/reset')
def reset_page():
    return render_template('reset.html')

from auth.db import users, otps
@app.route('/clear-data')
def clear_data():
    users.delete_many({})
    otps.delete_many({})
    return "All users deleted successfully"

# SINGLE TRANSACTION PREDICTION
@app.route('/predict', methods=['POST'])
def predict():

    data = request.json
    features = np.array(data['features'], dtype=float).reshape(1, -1)

    selected_model = data.get('model', 'hybrid')

    feature_names = ['Time'] + [f'V{i}' for i in range(1,29)] + ['Amount']
    features_df = pd.DataFrame(features, columns=feature_names)

    # Random Forest
    if selected_model == 'rf':
        prob = rf_model.predict_proba(features_df)[0][1]
        prediction = int(prob >= 0.30)

        return jsonify({
            'prediction': prediction,
            'probability': float(prob),
            'model_used': 'Random Forest',
            'accuracy': float(hybrid_cfg['rf_accuracy'])
        })

    # XGBoost
    if selected_model == 'xgb':
        prob = xgb_model.predict_proba(features_df)[0][1]
        prediction = int(prob >= hybrid_cfg['final_threshold'])

        return jsonify({
            'prediction': prediction,
            'probability': float(prob),
            'model_used': 'XGBoost',
            'accuracy': float(hybrid_cfg['xgb_accuracy'])
        })

    # LightGBM
    if selected_model == 'lgb':
        prob = lgb_model.predict_proba(features_df)[0][1]
        prediction = int(prob >= hybrid_cfg['final_threshold'])

        return jsonify({
            'prediction': prediction,
            'probability': float(prob),
            'model_used': 'LightGBM',
            'accuracy': float(hybrid_cfg.get('lgb_accuracy',0.9994))
        })

    # CatBoost
    if selected_model == 'cat':
        prob = cat_model.predict_proba(features_df)[0][1]
        prediction = int(prob >= hybrid_cfg['final_threshold'])

        return jsonify({
            'prediction': prediction,
            'probability': float(prob),
            'model_used': 'CatBoost',
            'accuracy': float(hybrid_cfg.get('cat_accuracy',0.9993))
        })

    # HYBRID MODEL
    rf_prob = rf_model.predict_proba(features_df)[0][1]
    xgb_prob = xgb_model.predict_proba(features_df)[0][1]
    lgb_prob = lgb_model.predict_proba(features_df)[0][1]
    cat_prob = cat_model.predict_proba(features_df)[0][1]

    rf_weight = hybrid_cfg['rf_accuracy']
    xgb_weight = hybrid_cfg['xgb_accuracy']
    lgb_weight = hybrid_cfg.get('lgb_accuracy',0.9994)
    cat_weight = hybrid_cfg.get('cat_accuracy',0.9993)

    final_prob = (
        rf_prob * rf_weight +
        xgb_prob * xgb_weight +
        lgb_prob * lgb_weight +
        cat_prob * cat_weight
    ) / (rf_weight + xgb_weight + lgb_weight + cat_weight)

    prediction = int(final_prob >= hybrid_cfg['final_threshold'])

    return jsonify({
        'prediction': prediction,
        'probability': float(final_prob),
        'rf_probability': float(rf_prob),
        'xgb_probability': float(xgb_prob),
        'lgb_probability': float(lgb_prob),
        'cat_probability': float(cat_prob),
        'model_used': 'Hybrid Model',
        'accuracy': float(max(rf_weight, xgb_weight, lgb_weight, cat_weight))
    })

# CSV DATASET FRAUD DETECTION
@app.route('/predict_csv', methods=['POST'])
def predict_csv():

    file = request.files['file']
    df = pd.read_csv(file)

    features = df.drop(columns=['Class'], errors='ignore')

    rf_probs = rf_model.predict_proba(features)[:,1]
    xgb_probs = xgb_model.predict_proba(features)[:,1]
    lgb_probs = lgb_model.predict_proba(features)[:,1]
    cat_probs = cat_model.predict_proba(features)[:,1]

    rf_weight = hybrid_cfg['rf_accuracy']
    xgb_weight = hybrid_cfg['xgb_accuracy']
    lgb_weight = hybrid_cfg.get('lgb_accuracy',0.9994)
    cat_weight = hybrid_cfg.get('cat_accuracy',0.9993)

    final_prob = (
        rf_probs * rf_weight +
        xgb_probs * xgb_weight +
        lgb_probs * lgb_weight +
        cat_probs * cat_weight
    )/(rf_weight + xgb_weight + lgb_weight + cat_weight)

    predictions = (final_prob >= hybrid_cfg['final_threshold']).astype(int)

    fraud_count = int(predictions.sum())
    total = len(predictions)

    return jsonify({
        "total_transactions": total,
        "fraud_detected": fraud_count,
        "legitimate": total - fraud_count,
        "fraud_rate": float((fraud_count/total)*100)
    })

# ===================== RUN =====================
#http://127.0.0.1:5000/clear-data
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)