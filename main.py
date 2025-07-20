from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("ODDS_API_KEY", "5294b7f0280bf731a841f498dd9e2907")
SPORT = "soccer_epl"  # Premier League
REGION = "eu"
BOOKMAKERS = ["pinnacle", "1xbet"]

@app.route("/")
def home():
    return "✅ Value Betting App is Running!"

@app.route("/valuebets")
def valuebets():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds?regions={REGION}&markets=h2h&oddsFormat=decimal&apiKey={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        return f"<h3>⚠️ API Error: {str(e)}</h3>"

    if isinstance(data, dict) and "error" in data:
        return f"<h3>⚠️ API Error: {data['error']}</h3>"

    rows = []
    for match in data:
        teams = " vs ".join(match["teams"])
        commence_time = match["commence_time"]
        league = match["sport_title"]

        # Extract Pinnacle & 1XBet odds
        pinnacle_odds = "-"
        x1bet_odds = "-"
        for bookmaker in match["bookmakers"]:
            if bookmaker["key"] == "pinnacle":
                pinnacle_odds = bookmaker["markets"][0]["outcomes"]
            elif bookmaker["key"] == "1xbet":
                x1bet_odds = bookmaker["markets"][0]["outcomes"]

        # Format nicely (just showing first team odds for now)
        pin_val = pinnacle_odds[0]["price"] if pinnacle_odds != "-" else "-"
        x1_val = x1bet_odds[0]["price"] if x1bet_odds != "-" else "-"

        rows.append(f"""
            <tr>
                <td>{teams}</td>
                <td>{league}</td>
                <td>{pin_val}</td>
                <td>{x1_val}</td>
                <td>{commence_time}</td>
            </tr>
        """)

    table_html = f"""
    <html>
        <head>
            <title>Value Bets</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background: #333; color: white; }}
            </style>
        </head>
        <body>
            <h2>📊 Pinnacle vs 1XBet Odds</h2>
            <table>
                <thead>
                    <tr>
                        <th>Match</th>
                        <th>League</th>
                        <th>Pinnacle</th>
                        <th>1XBet</th>
                        <th>Start Time</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        </body>
    </html>
    """
    return render_template_string(table_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
