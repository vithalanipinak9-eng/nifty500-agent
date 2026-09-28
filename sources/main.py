# main.py
"""
Nifty 500 News Agent - Phase 1
Monitors corporate announcements and sends high-impact alerts to Telegram.
"""

import time
from datetime import datetime
from config import POLL_INTERVAL_SECONDS, MIN_IMPACT_SCORE, MAX_ALERTS_PER_HOUR
from sources.announcements import fetch_recent_announcements, simple_impact_score
from telegram_bot import send_alert, send_telegram
from universe import get_watchlist

# Keep track of already sent alerts to avoid duplicates
sent_ids = set()
alerts_this_hour = 0
current_hour = datetime.now().hour

def run_once():
    global alerts_this_hour, current_hour
    
    now = datetime.now()
    if now.hour != current_hour:
        alerts_this_hour = 0
        current_hour = now.hour

    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Checking announcements...")
    
    announcements = fetch_recent_announcements(limit=40)
    print(f"  Found {len(announcements)} recent items")
    
    new_alerts = 0
    for item in announcements:
        uid = f"{item['symbol']}_{item['title'][:40]}"
        if uid in sent_ids:
            continue
            
        impact, score = simple_impact_score(item["title"], item["summary"])
        
        if score >= MIN_IMPACT_SCORE and alerts_this_hour < MAX_ALERTS_PER_HOUR:
            success = send_alert(
                symbol=item["symbol"],
                title=item["title"],
                summary=item["summary"][:300] + ("..." if len(item["summary"]) > 300 else ""),
                impact=impact,
                score=score,
                source=item["source"],
                link=item.get("link", "")
            )
            if success:
                sent_ids.add(uid)
                alerts_this_hour += 1
                new_alerts += 1
                print(f"  → Alert sent: {item['symbol']} ({impact}, {score})")
                time.sleep(1)
    
    if new_alerts == 0:
        print("  No new high-impact alerts")
    
    if len(sent_ids) > 500:
        sent_ids.clear()


def main():
    print("=" * 50)
    print("Nifty 500 News Agent started")
    print(f"Watching {len(get_watchlist())} symbols")
    print(f"Poll interval: {POLL_INTERVAL_SECONDS}s")
    print("=" * 50)
    
    send_telegram("🚀 <b>Nifty 500 News Agent is now running!</b>\n\nI will send you high-impact corporate announcements and news alerts here.")
    
    while True:
        try:
            run_once()
        except Exception as e:
            print(f"Error in main loop: {e}")
            send_telegram(f"⚠️ Agent error: {str(e)[:200]}")
        
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
