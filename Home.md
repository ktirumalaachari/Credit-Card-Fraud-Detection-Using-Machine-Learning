# 🏠 Credit Card Fraud Detection System Wiki

Welcome to the documentation for the Credit Card Fraud Detection System.  
This wiki covers system features, architecture, usage, and technical details.

---

## 📚 Table of Contents

- [🏠 Credit Card Fraud Detection System Wiki](#-credit-card-fraud-detection-system-wiki)
  - [📚 Table of Contents](#-table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [System Architecture](#system-architecture)
  - [Machine Learning Models](#machine-learning-models)
  - [Prediction Methods](#prediction-methods)
  - [Web Interface \& PWA](#web-interface--pwa)
  - [API Reference](#api-reference)
    - [`/predict`](#predict)
    - [`/predict_ensemble`](#predict_ensemble)
    - [`/predict_weighted`](#predict_weighted)
    - [`/predict_sequential`](#predict_sequential)
  - [Installation \& Deployment](#installation--deployment)
  - [FAQ](#faq)
  - [Contributing](#contributing)

---

## Overview

This project is a web-based, machine learning-powered system for detecting fraudulent credit card transactions.  
It supports eight ML models, Hybrid Model ensemble methods, interactive visualizations, and a mobile-friendly Progressive Web App (PWA) interface.

---

## Features

- Real-time fraud prediction (sub-500ms)
- 5 ML algorithms: Random Forest, XGBoost, LightGBM, CatBoost, Hybrid Model
- Ensemble, weighted, and sequential prediction methods
- Responsive dashboard and mobile PWA
- CSV upload and batch analysis
- Interactive charts (Plotly.js)
- Offline support and installable app

---

## System Architecture

- **Backend:** Python Flask
- **ML:** scikit-learn, XGBoost
- **Frontend:** HTML5, CSS3, JavaScript, Plotly.js
- **PWA:** Service Worker, Manifest
- **Model Storage:** Pickle (PKL), JSON (XGBoost)

---

## Machine Learning Models

|Short Name| Model Name            | Description                             |-----------------------------------------------------------------------------|
| rf        | Random Forest        | Ensemble of multiple decision trees that improves accuracy and reduces |overfitting.|
| xgb       | XGBoost              | Optimized and scalable gradient boosting algorithm for high-performance |prediction. |
| LGBM      | LightGBM             |
| CatB      | CatBoost             |
| hybrid    | Hybrid Model | Combines All Models using weighted probabilities for robust fraud detection. |

---

## Prediction Methods

- **Single Model:** Use one ML model for prediction.
- **Ensemble:** Majority voting between two models.
- **Weighted:** Weighted average based on model accuracy.
- **Sequential:** Second model used if first model’s confidence is low.

---

## Web Interface & PWA

- Responsive design for desktop and mobile
- Sidebar navigation for all pages
- PWA features: offline mode, install prompt, background sync
- Pages: Dashboard, Model, Visualizations, Analysis, Theory, Features, Amount Trends, Offline

---

## API Reference

### `/predict`  
**POST**: Single model prediction  
**Body:**  
```json
{
  "features": [0.5, -1.2, ...],  // 30 values
  "model": "rf"
}
```

### `/predict_ensemble`  
**POST**: Majority voting between two models  
**Body:**  
```json
{
  "features": [...],
  "model1": "rf",
  "model2": "xgb"
  "model3": "Lgbm"
  "model4": "CatB"
  "model5": "HyB"
}
```

### `/predict_weighted`  
**POST**: Weighted average prediction  
**Body:**  
```json
{
  "features": [...],
  "model1": "rf",
  "model2": "xgb"
  "model3": "Lgbm"
  "model4": "CatB"
  "model5": "HyB"
}
```

### `/predict_sequential`  
**POST**: Sequential prediction  
**Body:**  
```json
{
  "features": [...],
  "model1": "rf",
  "model2": "xgb",
  "model3": "Lgbm"
  "model4": "CatB"
  "threshold": 0.7
}
```

---

## Installation & Deployment

See [README.md](../README.md) for step-by-step instructions.

---

## FAQ

**Q:** What data format is required for predictions?  
**A:** 30 features: id, V1–V28, Amount.

**Q:** Can I use the app offline?  
**A:** Yes, core features are available offline via PWA.

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

For more details, explore the sidebar or open