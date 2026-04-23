from fastapi import FastAPI, Query
import nflreadpy as nfl
import pandas as pd

from app import custom_score_calc

app = FastAPI()

POS = ["QB", "RB", "WR", "TE", "K", "D/ST"]

# Loads player stats once on startup
seasons = [2025] # UPDATE 2025 with seasons you want to load
player_stats = nfl.load_player_stats(seasons=seasons).to_pandas()
# Converts inf and -inf to NaN, then fills NaN with 0 for JSON compatibility
player_stats = player_stats.replace([float('inf'), float('-inf')], pd.NA).fillna(0)

@app.get("/")
def test_route():
    return {"status": "API is running"}

@app.get("/ppr")
def get_ppr_points(pos: str = Query(..., description="Position filter, e.g., QB, RB, WR, TE, K, D/ST")):
    pos = pos.upper()

    # Ensures position is valid
    if pos not in POS:
        return {"error": f"Invalid position. Must be one of {POS}"}

    df = player_stats.copy()

    # Only includes regular season stats for the specified position
    df = df[df["season_type"] == "REG"] # Done here to keep team data, if done when loading stats, team data would be gone
    df = df[df["position"] == pos]

    # Calculate custom scoring for Kickers and Defense/Special Teams
    if pos == 'K':
        df = custom_score_calc.kicker_scoring(df)

    # Aggregates points by player, summing across teams for players who switched teams mid-season
    agg_df = df.groupby(
        ["player_id", "player_display_name", "position", "season"], as_index=False
    ).agg({
        "team": lambda x: "/".join(sorted(x.unique())),
        "fantasy_points_ppr": "sum"
    })

    # Sort by fantasy points descending
    agg_df = agg_df.sort_values(by="fantasy_points_ppr", ascending=False)

    return agg_df.to_dict(orient="records")
