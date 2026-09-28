# telegram_bot.py
import requests
from config import BOT_TOKEN, CHAT_ID

def send_telegram(text: str, parse_mode: str = "HTML") -> bool:
    """Send a message to the configured Telegram chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        return r.status_code == 200 and r.json().get("ok", False)
    except Exception as e:
        print(f"Telegram error: {e}")
        return False


def send_alert(symbol: str, title: str, summary: str, impact: str, score: int, source: str, link: str = ""):
    """Format and send a stock alert."""
    emoji = "🟢" if impact.lower().startswith("pos") else "🔴" if impact.lower().startswith("neg") else "⚪"
    
    text = f"""{emoji} <b>{symbol}</b> — {impact} (Score: {score}/10)

<b>{title}</b>

{summary}

Source: {source}
"""
    if link:
        text += f"\n<a href='{link}'>View details</a>"
    
    return send_telegram(text)
