# Backtest plan v2 · California floor votes

Written 2026-10-25, reviewed and approved the same day. It was committed to this registry before any of the following:
- the v2 code was written;
- the 2025–26 export settled (section 4);
- any 2025–26 vote table was downloaded.

This file's commit date is the evidence that the two fixes, the holdout and the gating came first. It will not be edited. Any change goes in a new dated file next to it, and applies only to results not yet seen.

## What this plan is

This plan follows `LEGISLATIVE-BACKTEST-PLAN-2026-10.md` (v1, registry `d5176e9`), its addendum `LEGISLATIVE-BACKTEST-ADDENDUM-2026-10-25.md` (`480f693`), and the phase 1 result published as `LEGISLATIVE-BACKTEST-RESULTS-PHASE1.md` (`637c13d`).

Phase 1 stands as published:

| Target | Phase 1 result | Why it failed |
|---|---|---|
| Passage | FAIL | Calibration. |
| Tally | FAIL | The 80% interval covered 38% of roll calls. |
| Member votes | PASS | — |

v2 changes what v1 allowed in four ways:
1. It adds two fixes, each fitted walk-forward.
2. It opens all eight sessions from 2009–10 to 2023–24 to development.
3. It names a new holdout, the 2025–26 session. This replaces v1 section 8's "2025–26 is never scored retroactively".
4. It gates member calls on the member target alone.

Everything v1 and the addendum fix and v2 does not change stays as written. That covers:
- the data sources and integrity rules;
- the unit, the forecast point and what may be used at it;
- the not-Aye tally;
- the features, the baselines and every threshold;
- the bootstrap and its seed.

## 1. What stays the same

- **The models.** The passage and member models are v1 section 5's: same features, same logistic regression, L2 penalty with C = 1.0.
- **The baselines.** B0, B1 and B2 are v1 section 4's, with the addendum's not-Aye tally.
- **The definitions.** Everything in addendum section 2 is unchanged.
- **The thresholds:**
  - passage: Brier skill ≥ 0.05; every scored bin within 0.05; ECE ≤ 0.03;
  - tally: MAE at least 10% lower; 80% interval coverage between 75% and 85%;
  - member votes: log-loss skill ≥ 0.05;
  - for each target, the 95% CI lower bound above 0 (or excluding 0) as in v1.
- **The point forecasts.** The tally's point forecast is still the sum of the members' not-Aye probabilities, so the tally MAE is computed exactly as in phase 1.

## 2. Fix 1: a calibration step for passage

**Method: isotonic regression**, fitted by the pool-adjacent-violators algorithm, on out-of-sample forecasts. Between the block midpoints the map is linear, and beyond the end blocks it is held flat.

**How it is fitted, walk-forward.** To score session *t*:
1. The passage model is fitted on every session before *t*, as in phase 1.
2. The calibration map is fitted on the pairs (forecast, outcome) for every session *s* before *t* except the first (2009–10). Each of those forecasts was made by a model fitted only on the sessions before *s*. These are the same out-of-sample forecasts a walk-forward run produces.
3. The calibrated forecast for each unit of *t* is the map applied to the model's forecast for that unit.

The map never sees session *t*. For the holdout (section 4), that means:
- the model is fitted on 2009–10 to 2023–24;
- the map is fitted on the out-of-sample forecasts for 2011–12 to 2023–24, seven sessions and 27,633 third-reading units.

**Why isotonic and not Platt scaling.**
- **The miscalibration is not one shift and one slope.** In phase 1 (pooled, fixed bins of width 0.1):
  - Forecasts of 0.1–0.2 were too high: mean forecast 0.139, observed 0.052.
  - Forecasts of 0.5–0.7 were too low: mean forecast 0.551 and 0.645, observed 0.765 and 0.906.
  - Forecasts above 0.8, which are most units, were close.
- **Platt scaling cannot fit that shape.** Platt scaling refits a slope and an intercept on the logit. It moves every forecast in the same direction along the logit scale, so it cannot pull the 0.1–0.2 band down while pushing the 0.5–0.7 band up.
- **Isotonic regression can.** It fits any order-preserving map. With 3,826 to 27,633 out-of-sample units behind each fit, it has enough data for a map of that kind.
- **Its weakness is overfitting where units are few.** The 0.1–0.8 range holds about 1,600 units across the five phase 1 sessions. To limit that, a block of the map is merged with its neighbor until it holds at least 30 units, the same minimum as for a scored bin.

**What it cannot do.** Isotonic regression keeps the model's order. In phase 1, units forecast below 0.1 passed more often (0.242 of 153) than units forecast at 0.1–0.2 (0.052 of 343). An order-preserving map can only pool those two bands together. If the calibrated forecasts still miss a scored bin by more than 0.05, passage fails again. That outcome is published as it is, and no second method is tried on the holdout.

**Scored as.** The calibrated forecasts replace the model's in every passage metric and in the pass rule. The uncalibrated model's scores are also reported, beside them.

## 3. Fix 2: a tally interval for votes that move together

**Why phase 1's interval failed.** It treated each member's vote as independent. On a real roll call:
- the members of a party move together, following leadership or a deal;
- absences cluster.

The Poisson-binomial is therefore far too narrow. Pooled coverage was 0.383, and no session reached 0.45.

**Method: a party-bloc effect on each roll call.**
- **The shift.** On roll call *r*, member *i*'s probability of not voting Aye is the member model's, shifted on the logit scale by *u*<sub>*r*,*g*</sub>. Here *g* is the member's party as `LEGISLATOR_TBL` records it: Democrat, Republican, or other/unknown.
- **The spread.** *u*<sub>*r*,*g*</sub> is drawn from a normal distribution with mean 0 and standard deviation σ<sub>house,*g*</sub>.
- **Independence.** Shifts for different parties on the same roll call are drawn independently.
- **Fitting the σ, walk-forward.** For each house and party, σ is the value that maximizes the likelihood of the observed party-bloc not-Aye counts, integrated over *u* with 40-point Gauss–Hermite quadrature. The data are the out-of-sample member forecasts on the roll calls of every session before *t* except the first. Their forecasts were made the same way as section 2's, so σ measures forecast error, not fitting error.
- **The interval.** For each roll call of session *t*:
  - draw 10,000 sets of shifts (seed 20261025);
  - draw the members' votes given each set;
  - take the 10th and 90th percentiles of the simulated not-Aye count.
- **The point forecast is unchanged.** It is still the sum of the unshifted probabilities, so MAE is the same as in phase 1.

**Why a bloc effect and not residual quantiles.** Residual quantiles would mean taking the 10th and 90th percentiles of (observed − forecast) from earlier sessions.
- That would give every roll call about the same width.
- The bloc effect makes the width depend on the bill:
  - on a bill where every member is forecast near certain Aye, a logit shift barely moves the count;
  - on a contested party-line bill, it moves the count a lot.
- That is the uncertainty a reader of a vote-count forecast needs.

**Its weakness.** It assumes one shift per party per roll call. Factions within a party, and absences that cut across parties, are not modeled. If coverage still falls outside 75–85%, the tally fails, and that is published.

**Reported beside it, not used in the pass rule:**
- phase 1's Poisson-binomial interval and its coverage;
- the fitted σ for each house and party, per session.

## 4. Development and the holdout

**Development: all eight sessions, 2009–10 to 2023–24.**
- Any of them may be used to develop and debug the two fixes, including the five sessions phase 1 tested.
- Results on these sessions are published as development results, labeled as such. They are not a test, and no pass or fail is declared on them.

**Holdout: the 2025–26 session.**
- **Never used before the scoring run.** It is not used for development, fitting, calibration or σ, nor looked at, before the single scoring run. This repository's only 2025–26 vote rows are those of the four bills in the platform.
- **The export.** The session ends on Nov 30, 2026. In v1's table, the exports for 2011–12 to 2023–24 are dated between Nov 25 and Dec 1 of the session's second year.
  - The holdout uses the export as it stands no earlier than Dec 2, 2026, and only once two HEAD requests a week apart return the same ETag.
  - A HEAD request records its ETag, size and Last-Modified in the lock file (section 7) before the download.
  - The download is then checked against them, as in v1 section 1.
- **Four bills excluded:** AB 566, SB 7, AB 412 and SB 1130.
  - Every unit of these bills (each house, and concurrence) is excluded from scoring.
  - Their roll calls still count in members' floor records before a later unit's forecast point, as any vote does.
  - These four bills' votes, authors, analyses and outcomes have been looked at in building the platform. Other 2025–26 bills have not.

**Pass rules on one session.** v1's rule that the model beat the best baseline in at least 4 of 5 sessions cannot be met by one session. It is replaced by the interval rule alone. For each target, all of these must hold on the holdout:

| Target | Rules |
|---|---|
| Passage | Brier skill against the best baseline ≥ 0.05, with the 95% CI lower bound above 0. Every bin of width 0.1 that holds at least 30 units within 0.05. ECE ≤ 0.03. |
| Tally | MAE at least 10% below the best baseline's, with the 95% CI of the difference excluding 0. 80% interval coverage between 75% and 85%. |
| Member votes | Log-loss skill against the best baseline ≥ 0.05, with the 95% CI lower bound above 0. |

The best baseline is the best on the holdout's scores. The bootstrap resamples bills within 2025–26, with 2,000 resamples and seed 20261025.

**This is a weaker test than v1's, and v2 says so plainly.**
- **The bootstrap misses variation between sessions.** It resamples bills within one session. It measures how much the score would vary with a different draw of that session's bills. It does not measure how much it varies from one session to the next.
- **Phase 1 showed that variation is real.** Tally coverage ranged from 0.298 to 0.449 across sessions, and calibration varies the same way.
- **What a pass shows.** A model that happened to suit 2025–26 can pass. Phase 1's rule asked for the same result in four sessions out of five, which a lucky session could not deliver alone.
- **Smaller bins are noisier.** One session also puts fewer units in each calibration bin. A bin is still scored with 30 units, but its observed rate is noisier than in a pooled five-session result. A fixed 0.05 tolerance is therefore harder to meet by chance and also easier to miss by chance.

**The live test: 2027–28.**
- For each target that passes on the holdout, forecasts for 2027–28 floor votes are locked in this registry at each unit's forecast point, as the election calls are. They are scored as the votes happen and in full when the session ends.
- The rules are the holdout's, unchanged.
- A target that fails the live test loses its display. The platform returns to "No forecast: not yet backtested" for what it covers, and that is published.

## 5. Gating, declared now

Each target gates its own display, independently:

| Display | Shown when |
|---|---|
| A passage probability | Passage passes. |
| A vote count, with its 80% interval | Tally passes. |
| A member-by-member call | Member votes pass. |

**What changes from v1.** v1 required passage and tally to pass before a vote count could be shown, and all three targets before a member call. Under v2:
- **A member call no longer depends on passage or tally.** Government-affairs teams use member calls on their own. They decide whom to lobby from each member's likely vote, not from the bill's chance of passing. A member call's accuracy is tested by the member target alone, and the bill's passage forecast does not enter it.
- **A vote count no longer depends on passage.** The tally is scored on its own roll calls, and its interval is what a count is shown with.

**What does not unlock a display.** Phase 1's member PASS does not unlock member calls. It was obtained under v1, whose gating it is reported under. Under v2, member calls are shown only after the member target passes on the 2025–26 holdout.

**How a member call is shown.** P(Aye) for each member, labeled as a forecast. It is never shown as a recorded vote, and never on the four excluded bills before their roll calls.

## 6. Phase 2

Phase 2 (registered opposition, v1 section 7) is not part of v2 and is not run under it. Whether and how it runs is a separate decision, made in a dated file before it is run.

## 7. Order of work

1. **Review and commit.** This file was reviewed, then committed and pushed to this registry, before anything below.
2. **Development.**
   - The two fixes are written in the platform repository and developed on 2009–10 to 2023–24.
   - The leakage test is extended to the calibration map and to σ: neither may change when a session's own outcomes are altered.
   - Development results are published here, labeled as development.
3. **Freeze.** The code is frozen and committed.
4. **Lock.** Once the 2025–26 export meets section 4 (no earlier than Dec 2, 2026; the same ETag a week apart), its HEAD request is recorded. A lock file in this registry then records:
   - the code's commit hash;
   - this file's SHA-256;
   - the export's ETag, size and Last-Modified;
   - the list of excluded bills.
5. **Score once.** The 2025–26 vote tables are downloaded, checked against the lock, extracted and scored once from the frozen commit. The full output is published here with its SHA-256, pass or fail, with the baselines' scores and everything v1 section 6 lists.
6. **Display, if anything passed.** Only for a target that passes, a platform change showing what that target allows (section 5) is proposed and reviewed on its own.
7. **Live test.** The 2027–28 live test follows section 4.
