# PULSE INTEL · Public Predictions Registry

This repository is the public, append-only record of PULSE INTEL's locked forecasts. A forecast is locked by committing it here before its election. The git history is the timestamp: anyone can check that a record, and the rules it will be scored by, existed before the result.

What it holds today: **11 forecasts for the November 3, 2026 general elections**, locked on 2026-10-08 under methodology v61.40, the methodology and its addendum, the rules they will be scored by, and a disclosure about earlier forecasts.

## The 11 locked forecasts

Locked 2026-10-08T03:40:41.902Z (commit `6d37251`), as of 2026-10-07, by build `pulse-intel-v6140.html` (SHA-256 `acca933752b328c06803ae6afd3615c731e134c6f949a328654bbb50ba5b7bb6`).

| Race | Principal candidates | Predicted winner | Lead (pts) | Win probability |
|---|---|---|---|---|
| [Florida Governor 2026](predictions/2026-11-03/fl-gov-gen.json) | Byron Donalds (R) vs David Jolly (D) | Byron Donalds | 2.69 | 71.8% |
| [Georgia Governor 2026](predictions/2026-11-03/ga-gov-gen.json) | Rick Jackson (R) vs Keisha Lance Bottoms (D) | Rick Jackson | 0.88 | 57.5% |
| [Georgia Senate 2026](predictions/2026-11-03/ga-sen-gen.json) | Jon Ossoff (D) vs Mike Collins (R) | Jon Ossoff | 9.32 | 97.7% |
| [Iowa Governor 2026](predictions/2026-11-03/ia-gov-gen.json) | Zach Lahn (R) vs Rob Sand (D) | Rob Sand | 8.30 | 96.2% |
| [Iowa Senate 2026](predictions/2026-11-03/ia-sen-gen.json) | Ashley Hinson (R) vs Josh Turek (D) | Josh Turek | 1.49 | 62.5% |
| [Maine Senate 2026](predictions/2026-11-03/me-sen-gen.json) | Susan Collins (R) vs Troy Jackson (D) | Troy Jackson | 2.22 | 68.3% |
| [Michigan Senate 2026](predictions/2026-11-03/mi-sen-gen.json) | Abdul El-Sayed (D) vs Mike Rogers (R) | Abdul El-Sayed | 2.90 | 73.3% |
| [North Carolina Senate 2026](predictions/2026-11-03/nc-sen-gen.json) | Roy Cooper (D) vs Michael Whatley (R) | Roy Cooper | 9.66 | 98.1% |
| [New Hampshire Senate 2026](predictions/2026-11-03/nh-sen-gen.json) | John E. Sununu (R) vs Chris Pappas (D) | Chris Pappas | 5.52 | 88.1% |
| [Ohio Senate 2026](predictions/2026-11-03/oh-sen-gen.json) | Jon Husted (R) vs Sherrod Brown (D) | Sherrod Brown | 3.86 | 79.6% |
| [Texas Senate 2026](predictions/2026-11-03/tx-sen-gen.json) | Ken Paxton (R) vs James Talarico (D) | James Talarico | 2.74 | 72.1% |

Each record also holds the margin as first-named minus second-named candidate, σ, the 80% and 95% margin ranges, the polls used with their weights, the eligibility check, and the SHA-256 of every input file. `predictions.json` indexes the 11 records.

## Methodology

[`METHODOLOGY-v61.40.md`](METHODOLOGY-v61.40.md), generated from the build's own outputs at lock time:

- **Polls only.** VoteHub, snapshot 2026-10-07T02:42:11Z. Partisan-sponsored and internal polls excluded; one row per fielding; a poll must give a number for both principal candidates.
- **Recency-weighted average.** Weight = 0.5^(age in days / 30) × the poll's 538 pollster weight. No house effects, no pollster grades.
- **σ = max(poll σ, 4.67)**, where 4.67 is the mean error of a polling average across 730 Senate and Governor generals, 1998–2022 (538 library). The floor binds in all 11 races, so win probability = Φ(margin / 4.67), and the ranges are margin ± 1.282 × 4.67 (80%) and ± 1.96 × 4.67 (95%).
- **Lock rule.** At least 8 polls after exclusions and the newest within 45 days; in Maine, two-way polls only. The races that failed it are listed in the methodology.
- **Not used:** fundamentals, expert ratings, sentiment, momentum, calibration.

[`METHODOLOGY-v61.40-addendum-2026-10-08.md`](METHODOLOGY-v61.40-addendum-2026-10-08.md) reports a walk-forward backtest of the same method on those 730 races, run after the locks. The day before the election, its 80% and 95% ranges held the result 70.8% and 88.9% of the time; coverage was lower at longer horizons. The locks were made 27 days out, so **their ranges are expected to be too narrow**. The records are unchanged and will be scored as locked.

## Scoring

[`SCORING-2026-GENERALS.md`](SCORING-2026-GENERALS.md), committed 2026-10-12 (commit `b020616`), before any result existed. It fixes:

- the SHA-256 each lock record must have;
- the certified-result format;
- when a race is not scored;
- the definitions (actual margin in points of all votes cast, winner call, error, range coverage, Brier score);
- the totals.

It pins the scorer, `score_generals_2026.py`, by its SHA-256; a copy is in [`verify/`](verify/). It will not be edited after the polls close; a change would be a new dated file, with both sets of scores published.

## Disclosure

[`DISCLOSURE-2026-09-28.md`](DISCLOSURE-2026-09-28.md) (extended 2026-10-07), with evidence in [`DISCLOSURE-2026-09-28-evidence.md`](DISCLOSURE-2026-09-28-evidence.md):

- **May primary forecasts.** The three primary forecasts locked here on 2026-05-09 were produced with simulated inputs, not the methodology published with them. They are not valid model forecasts.
- **June 29 primary calls.** These were written in an AI-assisted research session, not by the model.
- **May 26 general-election predictions.** This document was never published or locked, and it is withdrawn in full.

For the races it shares with the 11 above, the v61.40 locks are the only registered calls.

## Check it yourself

**When each record was made.** `git log --format='%h %cI %s' -- predictions/2026-11-03 SCORING-2026-GENERALS.md` shows the locks (committed 2026-10-08 03:40 UTC; git prints it in the committer's time zone, 2026-10-07 20:40 −07:00) and the scoring rules (2026-10-12), both before the election.

**That a record is unchanged.** `shasum -a 256 predictions/2026-11-03/*.json` should match the hashes listed in `SCORING-2026-GENERALS.md`.

**Reproduce the locks.** Everything needed is in [`verify/`](verify/): copies of the input files the records cite, byte for byte (credited in [`verify/ATTRIBUTION.md`](verify/ATTRIBUTION.md)), and a standalone script, Python 3 standard library only. From the registry root:

```sh
python3 verify/reproduce_locks.py
```

It first checks every input against the SHA-256 in the lock records, and the raw VoteHub responses against their manifest. It then recomputes each race from the inputs with the v61.40 method as `METHODOLOGY-v61.40.md` states it. It compares the leader, margin, win probability and both ranges with the record at stored precision, prints MATCH or MISMATCH per race, and exits non-zero on any mismatch. It writes nothing.

Each lock record also pins the SHA-256 of the platform build that produced it (`pulse-intel-v6140.html`, `acca9337…5ba7bb6`). The build itself is not public, so the script recomputes the locks from their inputs rather than from the build. Two other cited files, saved copies of a third party's web pages that no forecast uses, are not redistributed; their hashes are in `verify/ATTRIBUTION.md`.

**Run the scorer.** [`verify/score_generals_2026.py`](verify/score_generals_2026.py) is a byte-identical copy of the scorer that `SCORING-2026-GENERALS.md` pins. First check that it is that file:

```sh
shasum -a 256 verify/score_generals_2026.py
```

The output must be `2968815203484b8bd90c3636caa09563a24441ce1e80cfa7677d8acafc946b5e`, the hash in `SCORING-2026-GENERALS.md`. After the results are certified, put one result file per race in `results_2026/` at the registry root. The format is in `SCORING-2026-GENERALS.md`: each file is `<race_id>.json`, and the certified source documents go in `results_2026/sources/` with their SHA-256 in the result file. Then, from the registry root:

```sh
python3 verify/score_generals_2026.py --locks-dir predictions/2026-11-03 --results-dir results_2026 --json scores.json
```

The two flags are needed because the script's built-in defaults are the platform repository's layout. It refuses any race without a certified result, or whose lock record doesn't match its pinned hash, and says why. Until there are results, every race is reported as not scored.

## Older files

These are kept unchanged, because the registry is append-only, and are superseded:

- `predictions/2026-05-19/`: the three May primary records covered by the disclosure.
- `PRIMARY_METHODOLOGY.md`: the primary methodology published with them. The disclosure supersedes it.
- `lock_prediction.py`: the interactive tool used for those locks. Its docstring describes the withdrawn method. The 11 general-election records were written by the platform's lock script.
- `real_polls.json`: polls curated by hand in April 2026. No current forecast uses it.

## Append-only

A locked record is never edited, re-issued or deleted. Corrections and later findings go in new dated files beside the records (as the disclosure and the addendum do), and the git history keeps every version.

Questions: Jonathan Epstein, PULSE INTEL.
