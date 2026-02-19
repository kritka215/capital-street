import json
import os

LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), "leaderboard_data.json")

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_to_leaderboard(player_name, wealth, strategy):
    data = load_leaderboard()
    data.append({
        "name": player_name,
        "wealth": wealth,
        "strategy": strategy
    })
    # Sort by wealth descending
    data = sorted(data, key=lambda x: x["wealth"], reverse=True)
    # Keep top 10
    data = data[:10]
    
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)
