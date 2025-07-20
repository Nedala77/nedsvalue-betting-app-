from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Get API key from environment variable
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

@app.route("/")
def home():
    return "✅ Value Betting App is Running!"

@app.route("/valuebets")
def value_bets():
    # Example: Fetch Pinnacle odds via OddsAPI
    url = "https://api.the-odds-api.com/v4/sports/upcoming/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",          # Europe (1xbet usually included)
        "markets": "h2h",
        "oddsFormat": "decimal",
        "bookmakers": "pinnacle,1xbet"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": response.json()})

    data = response.json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
