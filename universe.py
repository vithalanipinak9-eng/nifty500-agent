# universe.py
# For Phase 1 we start with a solid Nifty 50 + some high-impact names.
# Full Nifty 500 list can be loaded later once we have a reliable free source.

NIFTY_50 = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "BHARTIARTL", "SBIN",
    "LICI", "ITC", "HINDUNILVR", "LT", "BAJFINANCE", "HCLTECH", "AXISBANK",
    "MARUTI", "SUNPHARMA", "TITAN", "NTPC", "ULTRACEMCO", "ADANIENT",
    "ONGC", "POWERGRID", "M&M", "WIPRO", "TATASTEEL", "COALINDIA", "NESTLEIND",
    "BAJAJFINSV", "ADANIPORTS", "JSWSTEEL", "TECHM", "HINDALCO", "INDUSINDBK",
    "GRASIM", "CIPLA", "DRREDDY", "BPCL", "APOLLOHOSP", "EICHERMOT", "DIVISLAB",
    "HEROMOTOCO", "BRITANNIA", "TATACONSUM", "SHREECEM", "HAVELLS", "PIDILITIND",
    "DABUR", "GODREJCP", "SIEMENS", "ABB"
]

# You can expand this list later with more Nifty 500 symbols
EXTRA_WATCH = [
    "ADANIGREEN", "ADANIPOWER", "TATAMOTORS", "ZOMATO", "PAYTM", "NYKAA",
    "DMART", "IRCTC", "PFC", "RECLTD", "BANKBARODA", "PNB", "CANBK"
]

def get_watchlist():
    return sorted(set(NIFTY_50 + EXTRA_WATCH))
