# sources/announcements.py
import requests
from datetime import datetime
from universe import get_watchlist

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nseindia.com/"
}

def get_nse_session():
    """Create a session with NSE cookies."""
    s = requests.Session()
    s.headers.update(HEADERS)
    try:
        s.get("https://www.nseindia.com", timeout=10)
    except:
        pass
    return s

def fetch_recent_announcements(limit=30):
    """
    Fetch recent corporate announcements from NSE.
    Returns list of dicts with symbol, title, summary, link, datetime.
    """
    results = []
    watch = set(get_watchlist())
    
    try:
        session = get_nse_session()
        url = "https://www.nseindia.com/api/corporate-announcements?index=equities"
        r = session.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            items = data if isinstance(data, list) else data.get("data", [])
            for item in items[:limit]:
                symbol = item.get("symbol") or item.get("sm_name") or ""
                symbol = symbol.upper().replace("-EQ", "").strip()
                if symbol and (symbol in watch or not watch):
                    results.append({
                        "symbol": symbol,
                        "title": item.get("desc") or item.get("subject") or item.get("attchmntText", "")[:120],
                        "summary": item.get("attchmntText") or item.get("desc") or "",
                        "link": item.get("attchmntFile") or item.get("url") or "",
                        "datetime": item.get("an_dt") or item.get("sort_date") or str(datetime.now()),
                        "source": "NSE Announcement"
                    })
    except Exception as e:
        print(f"NSE API error: {e}")

    return results


def simple_impact_score(title: str, summary: str) -> tuple[str, int]:
    """
    Rule-based impact scoring (1-10).
    Returns (impact_label, score)
    """
    text = (title + " " + summary).lower()
    
    positive_keywords = [
        "win", "order", "contract", "award", "approval", "launch", "expansion",
        "partnership", "acquisition", "profit", "growth", "dividend", "bonus",
        "upgrade", "record", "highest", "capacity", "investment", "mou", "deal"
    ]
    negative_keywords = [
        "loss", "decline", "penalty", "fine", "investigation", "fraud", "delay",
        "cancel", "suspend", "downgrade", "warning", "default", "layoff", "strike",
        "lawsuit", "probe", "sebi", "show cause"
    ]
    
    pos = sum(1 for k in positive_keywords if k in text)
    neg = sum(1 for k in negative_keywords if k in text)
    
    if pos > neg and pos >= 1:
        score = min(9, 5 + pos)
        return "Positive", score
    elif neg > pos and neg >= 1:
        score = min(9, 5 + neg)
        return "Negative", score
    else:
        return "Neutral", 4
