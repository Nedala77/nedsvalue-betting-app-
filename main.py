from flask import Flask, render_template_string
import requests, os

app = Flask(__name__)

API_KEY = os.getenv("ODDS_API_KEY", "5294b7f0280bf731a841f498dd9e2907")
SPORT = "soccer_epl"   # Can change to basketball_nba
REGION = "eu"

@app.route("/")
def home():
    return "✅ Sharp Over/Under Odds App Running!"

@app.route("/totals")
def totals():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds?regions={REGION}&markets=totals&oddsFormat=decimal&apiKey={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        return f"<h3>⚠️ API Error: {str(e)}</h3>"

    # If API error
    if isinstance(data, dict) and "error" in data:
        return f"<h3>⚠️ API Error: {data['error']}</h3><br>Raw: {data}"

    if not isinstance(data, list) or len(data) == 0:
        return "<h3>⚠️ No matches found (maybe API limit reached?)</h3>"

    rows = []
    for match in data:
        teams = " vs ".join(match.get("teams", ["Unknown", "Unknown"]))
        league = match.get("sport_title", "Unknown League")
        start_time = match.get("commence_time", "N/A")

        # Find Pinnacle totals market
        pinnacle_totals = "-"
        for bookmaker in match.get("bookmakers", []):
            if bookmaker.get("key") == "pinnacle":
                outcomes = bookmaker["markets"][0]["outcomes"]
                pinnacle_totals = ", ".join([f"{o['name']} {o['point']} @ {o['price']}" for o in outcomes])

        rows.append(f"""
            <tr>
                <td>{teams}</td>
                <td>{league}</td>
                <td>{pinnacle_totals}</td>
                <td>{start_time}</td>
            </tr>
        """)

    table_html = f"""
    <html>
        <head>
            <title>Over/Under Odds</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background: #333; color: white; }}
            </style>
        </head>
        <body>
            <h2>📊 Pinnacle Over/Under Odds ({SPORT})</h2>
            <table>
                <thead>
                    <tr>
                        <th>Match</th>
                        <th>League</th>
                        <th>Over/Under (Pinnacle)</th>
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
