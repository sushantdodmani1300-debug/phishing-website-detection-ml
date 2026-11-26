import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from features import extract_features
from predict import predict_url

st.set_page_config(page_title="Phishing URL Detector",page_icon="🔎",layout="centered")
st.title("🔎 Phishing Website Detection")
st.write("An educational machine-learning demo that analyzes URL text without opening or visiting the website.")
st.warning("Demo only: the model is trained on synthetic examples. Do not use this as a real cybersecurity decision tool.")

url=st.text_input("Enter a URL",placeholder="https://example.com")
if st.button("Analyze URL",type="primary",disabled=not url.strip()):
    try:
        result=predict_url(url.strip())
        if result["prediction"]=="Phishing-like":
            st.error(f"⚠️ Prediction: {result['prediction']}")
        else:
            st.success(f"✅ Prediction: {result['prediction']}")
        st.metric("Model confidence",f"{result['confidence']:.1%}")
        st.caption(f"Model: {result['model']}")
        with st.expander("URL features extracted"):
            st.dataframe(pd.DataFrame([extract_features(url)]).T.rename(columns={0:"Value"}))
        st.info("A legitimate-looking URL can still be malicious, and a suspicious-looking URL can be harmless. Verify through trusted sources.")
    except Exception as e:
        st.error(str(e))

st.divider()
st.subheader("How it works")
st.markdown("""
1. Extract URL features (length, tokens, dots, HTTPS, IP host, etc.).
2. Run the trained classification pipeline.
3. Display the predicted class and confidence score.
""")
