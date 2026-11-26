"""Feature extraction for URL strings. Does not fetch or visit URLs."""
import re
from urllib.parse import urlparse
from ipaddress import ip_address

SUSPICIOUS_WORDS = [
    "login", "verify", "secure", "account", "update", "bank", "confirm",
    "password", "signin", "wallet", "billing", "free", "bonus", "support"
]

def _parse_url(url: str):
    url = (url or "").strip()
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "http://" + url
    return url, urlparse(url)

def extract_features(url: str) -> dict:
    """Return numeric features from the URL text only."""
    normalized, parsed = _parse_url(url)
    host = parsed.hostname or ""
    try:
        ip_address(host)
        has_ip = 1
    except ValueError:
        has_ip = 0
    path = parsed.path or ""
    full = normalized.lower()
    labels = host.split(".") if host else []
    return {
        "url_length": len(normalized),
        "hostname_length": len(host),
        "path_length": len(path),
        "num_dots": normalized.count("."),
        "num_hyphens": normalized.count("-"),
        "num_underscores": normalized.count("_"),
        "num_at": normalized.count("@"),
        "num_question": normalized.count("?"),
        "num_equals": normalized.count("="),
        "num_ampersand": normalized.count("&"),
        "num_digits": sum(ch.isdigit() for ch in normalized),
        "num_percent": normalized.count("%"),
        "num_slashes": normalized.count("/"),
        "has_ip_address": has_ip,
        "uses_https": int(parsed.scheme.lower() == "https"),
        "has_port": int(parsed.port is not None) if parsed.port else 0,
        "subdomain_count": max(0, len(labels) - 2),
        "suspicious_word_count": sum(word in full for word in SUSPICIOUS_WORDS),
        "is_shortened_domain": int(any(s in host for s in ["bit.ly", "tinyurl", "t.co", "goo.gl", "ow.ly"])),
        "has_punycode": int("xn--" in host),
        "path_has_executable": int(any(ext in path.lower() for ext in [".exe", ".zip", ".scr", ".apk"])),
    }

FEATURE_NAMES = list(extract_features("https://example.com").keys())
