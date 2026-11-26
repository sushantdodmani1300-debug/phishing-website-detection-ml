"""Generate synthetic URL examples for an educational demonstration."""
from pathlib import Path
import random
import pandas as pd

RANDOM_SEED = 42
LEGIT_DOMAINS = [
    "wikipedia.org", "github.com", "python.org", "microsoft.com", "apple.com",
    "amazon.com", "bbc.com", "nytimes.com", "mit.edu", "openai.com",
]
PHISH_DOMAINS = [
    "secure-login-check.com", "account-verify-now.net", "bank-update-alert.org",
    "free-prize-confirm.xyz", "wallet-security-login.info", "support-billing-verify.co",
]
LEGIT_PATHS = ["/", "/about", "/products", "/help", "/docs", "/news", "/contact"]
PHISH_PATHS = [
    "/login/verify", "/account/update", "/secure/confirm", "/signin.php",
    "/bank/login", "/password/reset", "/billing/validate",
]

def make_data(n=2400):
    rng = random.Random(RANDOM_SEED)
    rows=[]
    for label in [0,1]:
        for i in range(n//2):
            if label == 0:
                domain=rng.choice(LEGIT_DOMAINS)
                path=rng.choice(LEGIT_PATHS)
                scheme=rng.choice(["https","https","https","http"])
                url=f"{scheme}://{domain}{path}"
                if rng.random() < .08: url += f"?page={rng.randint(1,20)}"
            else:
                domain=rng.choice(PHISH_DOMAINS)
                path=rng.choice(PHISH_PATHS)
                scheme=rng.choice(["http","https"])
                url=f"{scheme}://{rng.choice(['www.','secure.','verify.',''])}{domain}{path}"
                if rng.random() < .65:
                    url += f"?id={rng.randint(10000,99999)}&token={rng.choice(['abc','xyz','qwe'])}"
                if rng.random() < .12:
                    url = f"http://{rng.randint(10,240)}.{rng.randint(1,250)}.{rng.randint(1,250)}.{rng.randint(1,250)}/{path.strip('/')}"
            rows.append({"url":url, "label":label})
    rng.shuffle(rows)
    return pd.DataFrame(rows)

if __name__ == "__main__":
    out=Path(__file__).resolve().parents[1]/"data"/"urls.csv"
    out.parent.mkdir(exist_ok=True)
    make_data().to_csv(out,index=False)
    print(f"Created {out} ({len(make_data())} rows)")
