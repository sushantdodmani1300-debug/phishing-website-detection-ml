# Project Report Outline

## Title
Phishing Website Detection Using Machine Learning

## Problem statement
Phishing links imitate trusted services to trick people into sharing credentials or other information. This project demonstrates a machine-learning classification workflow that labels URL strings as phishing-like or legitimate-like based on lexical features.

## Objectives
- Build URL feature extraction without visiting URLs.
- Train and compare Logistic Regression, Decision Tree, and Random Forest.
- Evaluate on a held-out test set using accuracy, precision, recall, F1 and ROC-AUC.
- Create a working Streamlit prototype and CLI.

## Dataset
The included generator creates a balanced synthetic dataset. It is designed to demonstrate the ML workflow only and is not representative of the full variety of real-world URLs. For a production-quality academic study, replace it with a documented public dataset with clear license and provenance.

## Methodology
1. Generate or load data.
2. Extract numerical URL features.
3. Stratified 75/25 train-test split.
4. Train three models.
5. Select best model by F1-score.
6. Report metrics and confusion matrix.
7. Deploy locally using Streamlit.

## Features
Length and counts of URL characters, hostname and path lengths, HTTPS flag, IP-address host flag, subdomain count, suspicious-word count, shortened-domain flag, punycode flag and executable-file path flag.

## Evaluation
The training script reports Accuracy, Precision, Recall, F1 and ROC-AUC, plus a confusion matrix. Do not claim the metrics establish real-world protection because synthetic data is used.

## Limitations and ethics
- Synthetic data and intentionally simple patterns.
- Lexical URL-only features; no webpage or domain reputation checks.
- Potential false positives and false negatives.
- Never visit or interact with a suspicious URL for this demonstration.
- Predictions are informational only and not a security guarantee.
