import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
import xgboost as xgb
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

# Load dataset
df = pd.read_csv('backend/dataset/creditcard.csv')

X = df.drop('Class', axis=1)
y = df['Class']

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert back to DataFrame for CatBoost
X_train = pd.DataFrame(X_train, columns=X.columns)
X_test = pd.DataFrame(X_test, columns=X.columns)

# SMOTE (Handle imbalance)
smote = SMOTE(sampling_strategy=0.1, random_state=42)

X_train, y_train = smote.fit_resample(X_train, y_train)

# Random Forest
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

print("Training Random Forest...")
rf_model.fit(X_train, y_train)
print("Random Forest Done")

# XGBoost
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    eval_metric='logloss',
    random_state=42,
    n_jobs=-1
)

print("Training XGBoost...")
xgb_model.fit(X_train, y_train)
print("XGBoost Done")

# LightGBM
lgb_model = LGBMClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1
)

print("Training LightGBM...")
lgb_model.fit(X_train, y_train)
print("LightGBM Done")

# CatBoost
print("Training CatBoost...")

cat_model = CatBoostClassifier(
    iterations=100,
    depth=6,
    learning_rate=0.1,
    verbose=0
)

cat_model.fit(X_train, y_train)

print("CatBoost Done")

# Accuracy
rf_acc = accuracy_score(y_test, rf_model.predict(X_test))
xgb_acc = accuracy_score(y_test, xgb_model.predict(X_test))
lgb_acc = accuracy_score(y_test, lgb_model.predict(X_test))
cat_acc = accuracy_score(y_test, cat_model.predict(X_test))

# Save models
pickle.dump(rf_model, open('models/random_forest_model.pkl', 'wb'))
pickle.dump(xgb_model, open('models/xgboost_model.pkl', 'wb'))
pickle.dump(lgb_model, open('models/lightgbm_model.pkl', 'wb'))
pickle.dump(cat_model, open('models/catboost_model.pkl', 'wb'))

# Hybrid config
hybrid_thresholds = {
    "rf_threshold": 0.6,
    "xgb_threshold": 0.6,
    "final_threshold": 0.5,
    "rf_accuracy": rf_acc,
    "xgb_accuracy": xgb_acc,
    "lgb_accuracy": lgb_acc,
    "cat_accuracy": cat_acc
}

pickle.dump(hybrid_thresholds, open('backend/models/hybrid_thresholds.pkl', 'wb'))

print("Models saved successfully")
print("RF:", rf_acc)
print("XGB:", xgb_acc)
print("LGB:", lgb_acc)
print("CAT:", cat_acc)