#!/usr/bin/env python3
"""
lock_prediction.py — PULSE INTEL public registry helper

Generates a timestamped prediction JSON file ready to commit to the
pulse-intel-predictions public registry. Run this every time you lock
a prediction (10 days before each race resolves).

Usage:
    python3 lock_prediction.py

The script prompts you for the race details, generates the JSON entry,
saves it to predictions/YYYY-MM-DD/{race_id}.json, then prints the
git commands you should run to commit + push.

Methodology: PULSE INTEL composite-tuned 6-component ensemble.
Coefficients: polls 0.20, fundamentals 0.22, expert 0.29, approval 0.68,
sentiment 0.45, incumbency 1.0. Validated baseline (65-race library):
67.7% directional, 3.89pt MAE, 0.2373 Brier. Library expanded 2026-05-06
to 73 races; formal re-tuning against full library pending.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Constants — update these when methodology versions
METHODOLOGY_VERSION = "v1-composite-tuned-2026-04-25"
LIBRARY_VERSION = "73-race-2026-05-06"
COEFFICIENTS = {
    "polls": 0.20,
    "fundamentals": 0.22,
    "expert": 0.29,
    "approval_factor": 0.68,
    "sentiment_calibration": 0.45,
    "incumbency_advantage": 1.0,
}

# Race IDs match the PULSE INTEL platform's MARKET_DATA keys exactly.
# KY and AL Senate primaries use 'ky-senate-primary' and 'al-senate-primary'
# (no '-r-' suffix). GA Governor uses 'ga-gov-r-primary'.
RACES = {
    "ky-senate-primary": {
        "title": "Kentucky Senate Republican Primary 2026",
        "race_date": "2026-05-19",
        "candidates": ["Andy Barr", "Daniel Cameron", "Nate Morris"],
        "office": "U.S. Senate",
        "state": "KY",
        "primary_or_general": "primary",
        "runoff_possible": False,
    },
    "al-senate-primary": {
        "title": "Alabama Senate Republican Primary 2026",
        "race_date": "2026-05-19",
        "candidates": ["Barry Moore", "Steve Marshall", "Wes Hudson"],
        "office": "U.S. Senate",
        "state": "AL",
        "primary_or_general": "primary",
        "runoff_possible": True,
        "runoff_date": "2026-06-16",
    },
    "ga-gov-r-primary": {
        "title": "Georgia Governor Republican Primary 2026",
        "race_date": "2026-05-19",
        "candidates": ["Burt Jones", "Rick Jackson", "Brad Raffensperger", "Chris Carr"],
        "office": "Governor",
        "state": "GA",
        "primary_or_general": "primary",
        "runoff_possible": True,
        "runoff_date": "2026-06-16",
    },
    "ca-gov-jungle": {
        "title": "California Governor Jungle Primary 2026",
        "race_date": "2026-06-02",
        "candidates": ["Steve Hilton", "Tom Steyer", "Chad Bianco", "Xavier Becerra", "Katie Porter"],
        "office": "Governor",
        "state": "CA",
        "primary_or_general": "jungle_top_two",
        "runoff_possible": False,
    },
    "ia-senate-r-primary": {
        "title": "Iowa Senate Republican Primary 2026",
        "race_date": "2026-06-02",
        "candidates": ["Ashley Hinson", "Jim Carlin", "Joshua Smith"],
        "office": "U.S. Senate",
        "state": "IA",
        "primary_or_general": "primary",
        "runoff_possible": False,
    },
    "sc-gov-r-primary": {
        "title": "South Carolina Governor Republican Primary 2026",
        "race_date": "2026-06-09",
        "candidates": ["Alan Wilson", "Nancy Mace", "Pamela Evette", "Ralph Norman", "Rom Reddy"],
        "office": "Governor",
        "state": "SC",
        "primary_or_general": "primary",
        "runoff_possible": True,
        "runoff_date": "2026-06-23",
    },
}


def prompt(question, default=None):
    """Prompt with optional default value. Returns user input or default."""
    suffix = " [" + default + "]" if default else ""
    response = input(question + suffix + ": ").strip()
    return response if response else (default or "")


def generate_prediction(race_id, predicted_winner, predicted_margin_pts,
                        winner_probability_pct, predicted_runner_up=None,
                        confidence_interval_pts=None, notes=None):
    """Build a complete prediction JSON entry."""
    if race_id not in RACES:
        raise ValueError("Unknown race_id: " + race_id + ". Add it to RACES dict.")
    race = RACES[race_id]
    lock_dt = datetime.now(timezone.utc)
    race_dt = datetime.fromisoformat(race["race_date"] + "T00:00:00+00:00")
    days_before = (race_dt - lock_dt).days

    return {
        "schema_version": "1.0",
        "race_id": race_id,
        "race_title": race["title"],
        "race_date": race["race_date"],
        "office": race["office"],
        "state": race["state"],
        "primary_or_general": race["primary_or_general"],
        "candidates_in_field": race["candidates"],
        "lock_timestamp_utc": lock_dt.isoformat(),
        "lock_date": lock_dt.strftime("%Y-%m-%d"),
        "days_before_race": days_before,
        "prediction": {
            "predicted_winner": predicted_winner,
            "predicted_runner_up": predicted_runner_up,
            "predicted_margin_pts": predicted_margin_pts,
            "winner_probability_pct": winner_probability_pct,
            "confidence_interval_pts": confidence_interval_pts,
            "notes": notes or "",
        },
        "methodology": {
            "version": METHODOLOGY_VERSION,
            "library_version": LIBRARY_VERSION,
            "coefficients": COEFFICIENTS,
            "validated_baseline": {
                "directional_accuracy_pct": 67.7,
                "mean_absolute_error_pts": 3.89,
                "brier_score": 0.2373,
                "races_in_baseline": 65,
                "validation_locked_date": "2026-04-25",
            },
            "primary_ci_inflation": 1.5 if race["primary_or_general"] in ("primary", "jungle_top_two") else 1.0,
        },
        "runoff_possible": race.get("runoff_possible", False),
        "runoff_date": race.get("runoff_date"),
        "actual_result_pending": True,
    }


def main():
    print("")
    print("=" * 60)
    print("  PULSE INTEL — Lock a Prediction")
    print("=" * 60)
    print("")
    print("Available races:")
    for rid, r in RACES.items():
        print("  " + rid.ljust(28) + "  resolves " + r["race_date"] + "  (" + r["title"] + ")")
    print("")

    race_id = prompt("Race ID")
    if race_id not in RACES:
        print("")
        print("ERROR: '" + race_id + "' is not a known race.")
        print("Valid IDs are listed above. Copy one of those exactly.")
        sys.exit(1)

    race = RACES[race_id]
    print("")
    print("Race: " + race["title"])
    print("Field: " + ", ".join(race["candidates"]))
    print("")

    predicted_winner = prompt("Predicted winner (full name)")
    if not predicted_winner:
        print("ERROR: Predicted winner is required.")
        sys.exit(1)

    predicted_runner_up = prompt("Predicted runner-up (full name, optional)", default="")
    margin_str = prompt("Predicted margin (in points, e.g. 4.2)")
    try:
        predicted_margin_pts = float(margin_str)
    except ValueError:
        print("ERROR: Margin must be a number, e.g. 4.2 or 1.30")
        sys.exit(1)

    prob_str = prompt("Winner probability (in %, e.g. 67)")
    try:
        winner_probability_pct = float(prob_str)
    except ValueError:
        print("ERROR: Probability must be a number, e.g. 67 or 64.1")
        sys.exit(1)

    ci_str = prompt("Confidence interval +/- pts (optional, e.g. 3.5)", default="")
    confidence_interval_pts = float(ci_str) if ci_str else None
    notes = prompt("Notes (optional)", default="")

    prediction = generate_prediction(
        race_id=race_id,
        predicted_winner=predicted_winner,
        predicted_margin_pts=predicted_margin_pts,
        winner_probability_pct=winner_probability_pct,
        predicted_runner_up=predicted_runner_up or None,
        confidence_interval_pts=confidence_interval_pts,
        notes=notes,
    )

    out_dir = Path("predictions") / race["race_date"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / (race_id + ".json")

    with open(out_file, "w") as f:
        json.dump(prediction, f, indent=2)

    print("")
    print("Wrote " + str(out_file))
    print("")
    margin_disp = ("+" if predicted_margin_pts >= 0 else "") + str(predicted_margin_pts)
    print("  Prediction: " + predicted_winner + " wins by " + margin_disp + " pts (" + str(winner_probability_pct) + "% probability)")
    print("  Race date: " + race["race_date"] + " (" + str(prediction["days_before_race"]) + " days from lock)")
    print("  Methodology: " + METHODOLOGY_VERSION)
    print("")
    print("=" * 60)
    print("  Next: commit and push to make the prediction public")
    print("=" * 60)
    print("")
    print("  git add " + str(out_file))
    commit_msg = "Lock " + race_id + " prediction (" + race["race_date"] + ")"
    print("  git commit -m \"" + commit_msg + "\"")
    print("  git push")
    print("")
    print("  After all 3 races today, you can do them in one commit:")
    print("    git add predictions/2026-05-19/")
    print("    git commit -m \"Lock 2026-05-19 primary predictions: KY, AL, GA Gov\"")
    print("    git push")
    print("")


if __name__ == "__main__":
    main()
