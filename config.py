# config.py
# Sensitive credentials - do not share this file publicly

BOT_TOKEN = "8872182583:AAEASBMRllqQIoz7X91CKOcUv3Li9_3x8c0"
CHAT_ID = "8773542453"

# Settings
POLL_INTERVAL_SECONDS = 300          # Check every 5 minutes
MARKET_HOURS_ONLY = False            # Set True if you only want alerts during market hours
MIN_IMPACT_SCORE = 6                 # 1-10 scale. Only send alerts >= this score
MAX_ALERTS_PER_HOUR = 8              # Prevent spam

# For later expansion
WATCH_NIFTY_500 = True
WATCH_NIFTY_50 = True
