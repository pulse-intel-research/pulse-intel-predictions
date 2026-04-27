# PULSE INTEL · Public Predictions Registry

This is a public, append-only record of political forecasts made by **PULSE INTEL**, a bipartisan political analytics platform under development by Jonathan Epstein. Every prediction in this registry was committed to git **before** the corresponding race resolved, with timestamps that anyone can verify against this repo's git history.

---

## Why this registry exists

Political forecasting is a credibility-starved field. Most "forecasters" make predictions that are never publicly recorded, never closed-loop validated against actual results, and never accompanied by methodology disclosure. PULSE INTEL takes a different approach:

1. **Predictions are locked to this public registry before each race resolves**, using an automated tool (`lock_prediction.py`) that produces a structured git commit with timestamp.
2. **Actual results are recorded after each race resolves** using a companion tool (`record_actual.py`), which computes whether the prediction was correct and by how much.
3. **The methodology is fully documented** (see `PRIMARY_METHODOLOGY.md`) — including its limitations and where the model is being applied out-of-distribution.
4. **Every commit message follows a strict structured format** so the git log itself serves as an audit trail.

If you're evaluating PULSE INTEL as a vendor, sales asset, journalistic source, or methodology peer — start with the git log. Every prediction's pre-race lock commit is timestamped. Compare predicted vs actual via the per-race files in `predictions/`.

---

## What's currently tracked

**2026 primaries (5 flagship races):**

| Race | Primary Date | Lock Date | Status |
|------|--------------|-----------|--------|
| KY Senate (R) | May 19, 2026 | May 9, 2026 | Scheduled |
| AL Senate (R) | May 19, 2026 | May 9, 2026 | Scheduled |
| CA Governor | June 2, 2026 | May 23, 2026 | Scheduled |
| MI Senate | August 4, 2026 | July 25, 2026 | Scheduled |
| MN Senate | August 11, 2026 | August 1, 2026 | Scheduled |

**Status updates** are written to `predictions.json` and propagated to `predictions/<race_id>.json` on each lock and resolution.

---

## How to read this registry

### `predictions.json` — current state of all tracked races

A single file containing every race the platform has committed to forecasting, including:
- Locked predictions (winner, margin, confidence interval, methodology version)
- Actual results (after primary resolves)
- Computed accuracy metrics (called_correctly, margin_error_pts, within_confidence)
- Timestamps for every state transition

### `predictions/<race_id>.json` — durable per-race records

One file per race. **These files are append-only** — they accumulate fields as races progress through scheduled → locked → resolved. The original locked-prediction fields are never modified once written; only resolution fields are added.

### Git log — the audit trail

Every commit follows a structured message format:

```
Lock prediction: Kentucky Senate — Republican Primary

race_id:             ky-senate-r-primary-2026
primary_date:        2026-05-19
locked_at_utc:       2026-05-09T13:42:11+00:00
predicted_winner:    Andy Barr
predicted_margin:    +5.50 pts
confidence_interval: ±6.00 pts
methodology_version: v1-primary-2026

Locked via lock_prediction.py before any primary results were known.
```

To verify a prediction was made before a race: `git log --all --grep="<race_id>"`.

---

## About the methodology

**For primary forecasts:** see `PRIMARY_METHODOLOGY.md` in this repo for the full disclosure. Briefly:

- PULSE INTEL's underlying model (Composite-tuned ensemble) was calibrated against 65 general elections, not primaries. Applying it to primaries is **an out-of-distribution stretch**, and we say so explicitly in every primary forecast's methodology notes.
- Specific adjustments are made for primary use (incumbency zeroed, approval signal removed, sentiment signal removed, polls limited to independent pollsters, confidence interval widened 1.5x).
- The model's general-election performance — not yet tested in production but validated in a 65-race backtest (3.59 MAE, 72.3% direction, 90.9% governors-subset direction) — does not transfer guaranteed to primaries. Each primary forecast should be evaluated on its own merits, not against the general-election performance numbers.

**For general election forecasts (planned for November 2026):** the Composite-tuned methodology applies directly. Each November forecast will use `methodology_version: v1-composite-tuned` and the standard coefficients (polls 0.20, fundamentals 0.22, expert 0.29, approval 0.68, sentiment 0.45, incumbency 1.00).

---

## What this registry is NOT

- **Not a comprehensive forecast service.** Only the 5 flagship 2026 primaries (and forthcoming general-election scaffolds) are tracked here. PULSE INTEL the platform covers many more races; this registry is the subset where we've made formal locked predictions.
- **Not a real-time data feed.** Predictions are locked manually using `lock_prediction.py` on scheduled lock dates. Between locks, this registry doesn't change.
- **Not a substitute for the underlying analytics platform.** PULSE INTEL the SaaS prototype includes 16+ panels covering polling, fundamentals, geographic intelligence, messaging, fundraising, and more. This registry is specifically the closed-loop forecasting record.

---

## Tools used to maintain this registry

- **`lock_prediction.py`** — locks a prediction to the registry on the scheduled lock date (10 days before each primary). Refuses to overwrite existing locks without `--force`. Refuses to lock after the primary date. Generates structured commits.
- **`record_actual.py`** — records the actual result after a race resolves. Computes accuracy metrics. Refuses to record before the primary date. Generates structured commits.
- Both tools are open-source Python (no dependencies beyond stdlib + git). Available at: [scripts location TBD]

---

## Contact

For methodology questions, vendor inquiries, or peer review:

**Jonathan Epstein**
Building PULSE INTEL · 2026
[Contact info to be added]

---

*Last registry-level update: 2026-04-26*
*Next scheduled lock: KY Senate (R) primary, May 9, 2026*
