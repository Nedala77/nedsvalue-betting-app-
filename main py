from flask import Flask
import requests

# === CONFIG ===
ODDS_API_KEY = "5294b7f0280bf731a841f498dd9e2907"
TELEGRAM_BOT_TOKEN = "7895372454:AAFoIm490XAskKKsSmGm6KOWMHGp1g_PBbA"
TELEGRAM_CHAT_ID = "6564747718"
VALUE_THRESHOLD = 1.05  # 5% value

SPORT = "soccer_epl"
ODDS_URL = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={ODDS_API_KEY}&regions=eu&markets=h2h"

# === TELEGRAM ALERT ===
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, data=data)

# === GET ODDS ===
def fetch_odds():
    resp = requests.get(ODDS_URL)
    if resp.status_code != 200:
        return None, f"API Error: {resp.text}"
    return resp.json(), None

# === COMPARE ===
def find_value_bets(events):
    alerts = []

    for event in events:
        match = f"{event['home_team']} vs {event['away_team']}"
        pinnacle_odds, xbet_odds = {}, {}

        for book in event["bookmakers"]:
            if book["key"] == "pinnacle":
                for outcome in book["markets"][0]["outcomes"]:
                    pinnacle_odds[outcome["name"]] = outcome["price"]
            if book["key"] == "1xbet":
                for outcome in book["markets"][0]["outcomes"]:
                    xbet_odds[outcome["name"]] = outcome["price"]

        if pinnacle_odds and xbet_odds:
            for outcome in ["Home", "Draw", "Away"]:
                if outcome in pinnacle_odds and outcome in xbet_odds:
                    if xbet_odds[outcome] > pinnacle_odds[outcome] * VALUE_THRESHOLD:
                        alerts.append(
                            f"🔥 Value Bet!\n"
                            f"{match}\n"
                            f"{outcome}: Pinnacle {pinnacle_odds[outcome]} vs 1xBet {xbet_odds[outcome]}"
                        )

    return alerts

# === FLASK APP ===
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ ValueBet Bot is running! Go to /run to check bets."

@app.route("/run")
def run_bot():
    events, error = fetch_odds()
    if error:
        return f"❌ {error}"

    value_bets = find_value_bets(events)
    if value_bets:
        for bet in value_bets:
            send_telegram(bet)
        return f"✅ Sent {len(value_bets)} value bets to Telegram!"
    else:
        return "No value bets found."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
