import pandas as pd

"""
Calculates fantasy points for kickers based on nflreadpy data (kicking only)

Note - Some data from nflreadpy is incorrect for kickers, so points may not be exact
       (ie. Jason Meyers 2025 is listed as 196 PTS, when he should have 195 bc a missed field goal is not in the database)
"""
def kicker_scoring(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kicker Scoring:
    FG 0-19: +3
    FG 20-29: +3
    FG 30-39: +3
    FG 40-49: +4
    FG 50-59: +5
    FG 60+: +6

    Missed FG (all ranges): -1 each
    PAT made: +1
    PAT missed: -1
    """

    df = df.copy()

    # Ensure missing columns don't break
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")
        
    # Scoring Calculations
    # FG Made
    fg_made = (
        (df.get("fg_made_0_19", 0) * 3) +
        (df.get("fg_made_20_29", 0) * 3) +
        (df.get("fg_made_30_39", 0) * 3) +
        (df.get("fg_made_40_49", 0) * 4) +
        (df.get("fg_made_50_59", 0) * 5) +
        (df.get("fg_made_60_", 0) * 6)
    )
    # FG Missed
    fg_missed = (
        df.get("fg_missed_0_19", 0) +
        df.get("fg_missed_20_29", 0) +
        df.get("fg_missed_30_39", 0) +
        df.get("fg_missed_40_49", 0) +
        df.get("fg_missed_50_59", 0) +
        df.get("fg_missed_60_", 0)
    ) * -1
    # PAT Scoring
    pat_points = (
        df.get("pat_made", 0) * 1 +
        df.get("pat_missed", 0) * -1
    )
    # Total Score
    total = fg_made + fg_missed + pat_points

    # Overwrite Fantasy Fields
    df["fantasy_points"] = total
    df["fantasy_points_ppr"] = total

    return df
