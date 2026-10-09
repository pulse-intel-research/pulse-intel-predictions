# Methodology v61.40 — addendum, 2026-10-08: walk-forward backtest of the locked method

Addendum to [METHODOLOGY-v61.40.md](METHODOLOGY-v61.40.md). It reports a backtest run after the 2026-10-08 locks. **It changes nothing in them.**

## The v61.40 lock records are unchanged

The 11 records locked 2026-10-08T03:40:41.902Z (commit `6d37251`) are not edited, re-issued or superseded by this addendum. They will be scored as locked, against their recorded margins, win probabilities and intervals. On the evidence below, **their 80% and 95% intervals are expected to be too narrow**: the actual margin should be expected to fall outside them more often than 20% and 5% of the time.

## What was run

The production forecast function, `ensemblePredict()` in `pulse-intel-v6140.html` (SHA-256 `acca933752b328c06803ae6afd3615c731e134c6f949a328654bbb50ba5b7bb6`, the locked build), in the exact v61.40 configuration: polls only, recency weight 0.5^(age/30), 538 pollster weights, σ = max(poll σ, 4.67). Nothing in the model was reimplemented or altered.

- **Races:** the 730 Senate and Governor generals, 1998–2022, of the 538 library from which the 4.67 floor is computed. Their dated polls (4,839) come from the archived 538 raw-polls file `data/538/pollster-ratings__2023__raw-polls.csv` (SHA-256 `f637423f4b17ad7f4506c5fc3884056e6b32fcbc97e67291c4b078cd6a2d5283`). The join reproduces the library's poll counts, averages and actual margins for every race.
- **Walk-forward:** at each horizon T−h, a race sees only polls dated at least h days before its election. A race with no poll yet is not scored.
- **Harness:** `harnesses/10-walkforward-v6140.js` in the platform repo (commits `c0b8683`, `b0b2be9`). It runs with the rest of the harness suite on every build.

## Results

| As of | Races scored | MAE (pts) | MAE of the plain poll average, same polls | Winner called | Inside 80% interval | Inside 95% interval |
|---|---|---|---|---|---|---|
| T−1 | 730 | 4.53 | 4.67 | 91.5% | **70.8%** | **88.9%** |
| T−7 | 707 | 4.78 | 4.92 | 90.9% | 68.6% | 86.3% |
| T−14 | 575 | 5.10 | 5.18 | 87.1% | 68.0% | 83.8% |

At T−7 and T−14, 23 and 155 races had no poll yet and are not scored. At T−14, two forecasts of exactly zero margin are counted as wrong calls. The σ floor bound in every scored race at every horizon, so every interval is margin ± 1.282 × 4.67 (80%) or ± 1.96 × 4.67 (95%), as in the lock records.

## Findings

**The intervals cover too little.** The day before the election, 70.8% of actual results fell inside the 80% interval and 88.9% inside the 95% interval. Coverage falls further at longer horizons.

**Why: the floor is an MAE used as a σ.** 4.67 is the library's mean absolute error of a polling average. The method uses it as the standard deviation of a normal distribution. For a normal error with mean zero, the mean absolute error is σ·√(2/π), so the σ that matches an MAE of 4.67 is 4.67 × √(π/2) ≈ **5.85**, not 4.67. Using the MAE as σ makes every interval about 20% too narrow by construction.

**Winner calls are no better than a plain average.** 91.5% at T−1 is the same rate as the unweighted average of the same polls (the library's 91.5%). The weighting lowers MAE slightly (4.53 vs 4.67 at T−1) but does not call more races correctly.

**The MAE gain is in-sample.** The 538 pollster weights are derived from 538's pollster ratings, which were fitted in part on the errors of these same historical polls. The weights therefore had sight of the outcomes they are tested on, and the 4.53 vs 4.67 improvement is an optimistic estimate. The 4.67 floor is likewise computed from these same 730 races, so the intervals are not tested out of sample either.

**The backtest cannot reach the live horizon.** The locked forecasts are as of 2026-10-07, 27 days before the 2026-11-03 election (T−27). 538's raw-polls file keeps only polls from the final 21 days of each race, so no historical race can be forecast at T−27. Coverage falls as the horizon lengthens (70.8% → 68.0% at 80%; 88.9% → 83.8% at 95%, from T−1 to T−14). The T−1 to T−14 figures are therefore best read as upper bounds on how well the locked intervals will cover at T−27.

## Poll dates

538's `polldate` is the **median field date** of a poll. That is 538's own definition, and it was confirmed against the published fieldwork of Marist PA and GA 2022 (Oct 31–Nov 2, `polldate` 11/1) and Selzer IA 2020 (Oct 26–29, `polldate` 10/28). It also sat on the true midpoint for 96.4% of the 112 polls that could be matched to 538's state-of-the-polls start and end dates. The method ages a poll from its **end** date, which the raw file does not carry; typical fieldwork is 2 days. Rerunning with every end date assumed 1 or 2 days after `polldate` left the T−1 results at MAE 4.53 / 4.57 and coverage 70.5% / 88.9% and 70.4% / 88.8%. The findings above do not depend on this.

## Also noted

The 538 library's provenance text says `avg_poll_margin` is rounded to 1 decimal place. 390 of its 730 rows are stored to 2, with exact halves rounded half-to-even. Every row agrees with the raw polls at its stored precision. This affects no number in the forecasts.
