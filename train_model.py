"""Train and evaluate multiple models on synthetic URL examples."""
from pathlib import Path
import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from features import extract_features, FEATURE_NAMES

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"urls.csv"
MODELS=ROOT/"models"
REPORTS=ROOT/"reports"

def main():
    if not DATA.exists():
        from generate_dataset import make_data
        make_data().to_csv(DATA,index=False)
    df=pd.read_csv(DATA)
    X=pd.DataFrame([extract_features(u) for u in df.url])
    y=df.label.astype(int)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    models={
        "Logistic Regression":Pipeline([("scale",StandardScaler()),("model",LogisticRegression(max_iter=1000))]),
        "Decision Tree":DecisionTreeClassifier(max_depth=8,random_state=42),
        "Random Forest":RandomForestClassifier(n_estimators=180,max_depth=10,random_state=42,class_weight="balanced"),
    }
    metrics={}
    best_name,best_model,best_f1=None,None,-1
    for name,model in models.items():
        model.fit(X_train,y_train)
        pred=model.predict(X_test)
        proba=model.predict_proba(X_test)[:,1]
        result={
            "accuracy":float(accuracy_score(y_test,pred)),
            "precision":float(precision_score(y_test,pred,zero_division=0)),
            "recall":float(recall_score(y_test,pred,zero_division=0)),
            "f1":float(f1_score(y_test,pred,zero_division=0)),
            "roc_auc":float(roc_auc_score(y_test,proba)),
        }
        metrics[name]=result
        if result["f1"]>best_f1:
            best_name,best_model,best_f1=name,model,result["f1"]
    MODELS.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True)
    joblib.dump({"model":best_model,"features":FEATURE_NAMES,"model_name":best_name},MODELS/"phishing_model.joblib")
    (REPORTS/"model_metrics.json").write_text(json.dumps({"best_model":best_name,"models":metrics},indent=2))
    cm=confusion_matrix(y_test,best_model.predict(X_test))
    fig,ax=plt.subplots(figsize=(5,4))
    ax.imshow(cm)
    ax.set_title(f"Confusion Matrix — {best_name}")
    ax.set_xlabel("Predicted label"); ax.set_ylabel("Actual label")
    ax.set_xticks([0,1],["Legitimate-like","Phishing-like"])
    ax.set_yticks([0,1],["Legitimate-like","Phishing-like"])
    for (i,j),v in __import__("numpy").ndenumerate(cm): ax.text(j,i,str(v),ha="center",va="center")
    fig.tight_layout(); fig.savefig(REPORTS/"confusion_matrix.png",dpi=150); plt.close(fig)
    print(json.dumps({"best_model":best_name,"metrics":metrics},indent=2))
if __name__=="__main__": main()
