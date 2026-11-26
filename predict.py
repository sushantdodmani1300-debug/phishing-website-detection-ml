"""Command line URL prediction."""
from pathlib import Path
import argparse, joblib, pandas as pd
from features import extract_features

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/"models"/"phishing_model.joblib"

def predict_url(url):
    if not MODEL.exists():
        raise FileNotFoundError("Model missing. Run: python src/train_model.py")
    pack=joblib.load(MODEL)
    X=pd.DataFrame([extract_features(url)])
    model=pack["model"]
    label=int(model.predict(X)[0])
    confidence=float(model.predict_proba(X)[0][label])
    return {"prediction":"Phishing-like" if label else "Legitimate-like","confidence":confidence,"model":pack["model_name"]}

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Educational URL phishing classifier")
    parser.add_argument("url",help="URL to classify (no network request will be made)")
    args=parser.parse_args()
    result=predict_url(args.url)
    print(f"Prediction: {result['prediction']} | Confidence: {result['confidence']:.1%} | Model: {result['model']}")
