# Scoring rules · November 2026 general elections

Written 2026-10-12, before any result exists. This file's commit date in this registry is the evidence that the rules came first. It will not be edited after the polls close on 2026-11-03. If a rule ever has to change, the change goes in a new dated file next to this one, and both sets of scores are published.

The scorer is `score_generals_2026.py` in the platform repository (pulse-intel-research/pulse-intel-prototype), SHA-256 `2968815203484b8bd90c3636caa09563a24441ce1e80cfa7677d8acafc946b5e`. It implements these rules and nothing else; a scorer with any other hash is not the one these rules describe.

## What is scored

The 11 forecasts locked on 2026-10-08 under methodology v61.40 (registry commit `6d37251`). Each record is scored as locked. A record is scored only if its file's SHA-256 equals the value below; otherwise that race is not scored.

| Race | Record | SHA-256 | Margin is | Locked margin | 80% range | 95% range | Predicted winner | Win probability |
|---|---|---|---|---|---|---|---|---|
| fl-gov-gen | `predictions/2026-11-03/fl-gov-gen.json` | `f9ea45ccd56f750d211255a7e8e0de9c6c9c11cea0535896f3eb86277ae05b40` | Byron Donalds (R) − David Jolly (D) | 2.69 | −3.30 to 8.68 | −6.46 to 11.84 | Byron Donalds | 71.8% |
| ga-gov-gen | `predictions/2026-11-03/ga-gov-gen.json` | `6442cba22035f6bff497dc65ccb941a0e830906c06344b1e0048902a647cac4e` | Rick Jackson (R) − Keisha Lance Bottoms (D) | 0.88 | −5.11 to 6.87 | −8.27 to 10.03 | Rick Jackson | 57.5% |
| ga-sen-gen | `predictions/2026-11-03/ga-sen-gen.json` | `95eaedc42168f263740e6302b20fdc1ede26c85e2f53dd534295ae555b60a995` | Jon Ossoff (D) − Mike Collins (R) | 9.32 | 3.33 to 15.31 | 0.17 to 18.47 | Jon Ossoff | 97.7% |
| ia-gov-gen | `predictions/2026-11-03/ia-gov-gen.json` | `ced89a266c0d7ec7292f7a2cac67c3da545de346d129c7c03f62f4917f3b635b` | Zach Lahn (R) − Rob Sand (D) | −8.30 | −14.29 to −2.31 | −17.45 to 0.85 | Rob Sand | 96.2% |
| ia-sen-gen | `predictions/2026-11-03/ia-sen-gen.json` | `4864f3171106f3e50bcc09d04bfe56c0f26d1d7974ff8dcf65cefb019647c019` | Ashley Hinson (R) − Josh Turek (D) | −1.49 | −7.48 to 4.50 | −10.64 to 7.66 | Josh Turek | 62.5% |
| me-sen-gen | `predictions/2026-11-03/me-sen-gen.json` | `c7658cd4ec271aa43aa67dcc5b3dd53396eadcc9fbfe75f7f9463ffd466722a1` | Susan Collins (R) − Troy Jackson (D) | −2.22 | −8.21 to 3.77 | −11.37 to 6.93 | Troy Jackson | 68.3% |
| mi-sen-gen | `predictions/2026-11-03/mi-sen-gen.json` | `0303196e9c088f52244418e50e7aab88478b616a00e2c61eafe74641666447d6` | Abdul El-Sayed (D) − Mike Rogers (R) | 2.90 | −3.09 to 8.89 | −6.25 to 12.05 | Abdul El-Sayed | 73.3% |
| nc-sen-gen | `predictions/2026-11-03/nc-sen-gen.json` | `4e1c019509b3853247939fc3f0e4bc473303d7689786b0971a7f6f99cbc23869` | Roy Cooper (D) − Michael Whatley (R) | 9.66 | 3.67 to 15.65 | 0.51 to 18.81 | Roy Cooper | 98.1% |
| nh-sen-gen | `predictions/2026-11-03/nh-sen-gen.json` | `85666d16b7562fc78bf190e4053e0eb63f0e3984990607bc110d607ac881eaa4` | John E. Sununu (R) − Chris Pappas (D) | −5.52 | −11.51 to 0.47 | −14.67 to 3.63 | Chris Pappas | 88.1% |
| oh-sen-gen | `predictions/2026-11-03/oh-sen-gen.json` | `6c8b4409fb50df3a7dfc0032d0c39b9a13529da2b51f856d07ca4ac86b206eca` | Jon Husted (R) − Sherrod Brown (D) | −3.86 | −9.85 to 2.13 | −13.01 to 5.29 | Sherrod Brown | 79.6% |
| tx-sen-gen | `predictions/2026-11-03/tx-sen-gen.json` | `56288682172161efe642ac053e8a6c1df15e48102bbb985e2d2ea2e8bd2d8821` | Ken Paxton (R) − James Talarico (D) | −2.74 | −8.73 to 3.25 | −11.89 to 6.41 | James Talarico | 72.1% |

Every margin above is the first-named candidate minus the second, in percentage points. The win probability is the locked probability that the predicted winner wins.

## The result for each race

One file per race, `data/results_2026/<race_id>.json` in the platform repository, holding the certified result:

| Field | Meaning |
|---|---|
| `race_id` | as above |
| `certified` | `true`; a result that has not been certified is not scored |
| `certified_date` | the date the result was certified |
| `round` | `general` for every race except `me-sen-gen`, which is `rcv-final` (see below) |
| `d_candidate`, `r_candidate` | the two principal candidates, named exactly as in the lock record |
| `d_votes`, `r_votes` | their certified vote totals |
| `total_votes` | certified total votes cast for the office, all candidates (for `me-sen-gen`, continuing ballots in the final round) |
| `source_url` | where the certified result was published |
| `retrieved` | the date it was retrieved |
| `source_file` | the certified document as retrieved, saved under `data/results_2026/sources/` |
| `sha256` | the SHA-256 of `source_file` |

A race is not scored, and the scorer says why, if: there is no result file; it is not certified; a field is missing; the candidates don't match the lock record; the vote totals are inconsistent (the two candidates' votes exceed the total); the source document is missing or its SHA-256 doesn't match; or the lock record's SHA-256 doesn't match the table above. Test fixtures carry `"fixture": true` and are never scored as results.

**Maine Senate** is scored on the ranked-choice final round, because the lock used only two-way polls (head-to-head questions or ranked-choice final rounds).

**Georgia** (Senate and Governor) is scored on the November 3 count. If a race goes to a runoff, the runoff is not scored: the lock forecast the November 3 margin.

## Definitions

- **Actual margin** = 100 × (votes for the first-named candidate − votes for the second) ÷ `total_votes`, in points of all votes cast. That is the scale of the locked polling margin and of the 538 library's actual margins, on which the method's σ was set.
- **Winner called right**: the predicted winner received more votes than the other principal candidate. An exact tie is not a correct call (as in the v61.40 addendum).
- **Error** = actual margin − locked margin, in the table's direction. Absolute error = |error|.
- **Inside the 80% / 95% range**: the actual margin lies within the locked `margin_interval_80` / `margin_interval_95`, endpoints included, as recorded in the lock record.
- **Brier score** = (p − o)², where p is the locked win probability of the predicted winner (as a fraction) and o is 1 if the winner was called right, 0 if not (0.5 for an exact tie). Lower is better; always forecasting 50% scores 0.25.

## Totals

Over the races scored (with the count, and the races not scored and why):

- winners called right, out of the number scored;
- mean absolute error and mean signed error of the margin;
- 80% and 95% coverage: the share of results inside each range, shown against the nominal 80% and 95%. The v61.40 addendum (2026-10-08) found these ranges too narrow: in a walk-forward backtest the day before the election, 70.8% of results fell inside the 80% range and 88.9% inside the 95% range, and coverage was lower at longer horizons. These locks were made 27 days out, so coverage below nominal is expected. With 11 races, coverage is a count out of 11, not a precise rate;
- mean Brier score.

Numbers are computed at full precision and reported to two decimal places (margins and errors) and four (Brier).
