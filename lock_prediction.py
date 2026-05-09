#!/usr/bin/env python3
"""
lock_prediction.py — PULSE INTEL public registry helper

Generates a timestamped prediction JSON file ready to commit to the
pulse-intel-predictions public registry. Run this every time you lock
a prediction (10 days before each race resolves).

Usage:
    python3 lock_prediction.py

The script will prompt you for the race details, generate the JSON
entry, save it to the correct path, and print the git commands.

Methodology: PULSE INTEL composite-tuned 6-component ensemble.
Coefficients: polls 0.20, fundamentals 0.22, expert 0.29, approval 0.68,
sentiment 0.45, incumbency 1.0. Validated baseline (65-race library):
67.7% directional, 3.89pt MAE, 0.2373 Brier. Library expanded 2026-05-06
to 73 races; formal re-tuning against full library pending.
"""

import json
import os
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

# Known active 2026 races — for quick lookup. Update as new races are added.
RACES = {
    "ky-senate-r-primary": {
        "title": "Kentucky Senate Republican Primary 2026",
        "race_date": "2026-05-19",
        "candidates": ["Andy Barr", "Daniel Cameron", "Nate Morris"],
        "office": "U.S. Senate",
        "state": "KY",
        "primary_or_general": "primary",
        "runoff_possible": False,
    },
    "al-senate-r-primary": {
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
    """Prompt with optional default value."""
    suffix = f" [{default}]" if default else ""
    response = input(f"{question}{suffix}: ").strip()
    return response if response else (default or "")


def generate_prediction(race_id, predicted_winner, predicted_margin_pts,
                         winner_probability_pct, predicted_runner_up=None,
                         confidence_interval_pts=None, notes=None):
    """Build a complete prediction JSON entry."""
    if race_id not in RACES:
        raise ValueError(f"Unknown race_id: {race_id}. Add it to RACES dict.")
    race = RACES[race_id]

    # Lock timestamp — UTC ISO 8601
    lock_dt = datetime.now(timezone.utc)

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
        "days_before_race": (datetime.fromisoformat(race["race_date"] + "T00:00:00+00:00") - lock_dt).days,
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
    print("\n" + "=" * 60)
    print("  PULSE INTEL — Lock a Prediction")
    print("=" * 60 + "\n")

    # Show available races
    print("Available races:")
    for rid, r in RACES.items():
        print(f"  {rid:30s}  resolves {r['race_date']}  ({r['title']})")
    print()

    race_id = prompt("Race ID")
    if race_id not in RACES:
        print(f"\nERROR: '{race_id}' is not a known race. Add it to the RACES dict in this script.")
        sys.exit(1)

    race = RACES[race_id]
    print(f"\nRace: {race['title']}")
    print(f"Field: {', '.join(race['candidates'])}\n")

    predicted_winner = prompt("Predicted winner (full name)")
    predicted_runner_up = prompt("Predicted runner-up (full name, optional)", default="")
    predicted_margin_pts = float(prompt("Predicted margin (in points, e.g. 4.2)"))
    winner_probability_pct = float(prompt("Winner probability (in %, e.g. 67)"))
    ci_str = prompt("Confidence interval +/- pts (optional, e.g. 3.5)", default="")
    confidence_interval_pts = float(ci_str) if ci_str else None
    notes = prompt("Notes (optional, e.g. 'runoff likely; this is round-1 winner')", default="")

    # Build prediction
    prediction = generate_prediction(
        race_id=race_id,
        predicted_winner=predicted_winner,
        predicted_margin_pts=predicted_margin_pts,
        winner_probability_pct=winner_probability_pct,
        predicted_runner_up=predicted_runner_up or None,
        confidence_interval_pts=confidence_interval_pts,
        notes=notes,
    )

    # Save to predictions/YYYY-MM-DD/{race_id}.json
    out_dir = Path("predictions") / race["race_date"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{race_id}.json"

    with open(out_file, "w") as f:
        json.dump(prediction, f, indent=2)

    print(f"\n✓ Wrote {out_file}")
    print(f"\n  Prediction: {predicted_winner} wins by {predicted_margin_pts:+.1f} pts ({winner_probability_pct:.0f}% probability)")
    print(f"  Race date: {race['race_date']} ({prediction['days_before_race']} days from lock)")
    print(f"  Methodology: {METHODOLOGY_VERSION}")

    print("\n" + "=" * 60)
    print("  Next: commit and push to make the prediction public")
    print("=" * 60 + "\n")
    print(f"  git add {out_file}")
    print(f'  git commit -m "Lock {race_id} prediction ({race[\"race_date\"]})"')
    print(f"  git push")
    print()
    print("  After the race resolves, run record_actual.py with the result.")
    print()


if __name__ == "__main__":
    main()
