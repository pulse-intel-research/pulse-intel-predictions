# Disclosure — 2026-09-28

## The three forecasts locked on 2026-05-09 were not produced by the published methodology

The forecasts locked on 2026-05-09 for the Kentucky Senate, Alabama Senate and Georgia Governor Republican primaries (race date 2026-05-19) were not made the way this registry describes.

They were produced by the PULSE INTEL prototype, build v48.1, with its poll input switched off. The three inputs that carried weight — fundamentals, expert ratings and sentiment — were simulated placeholder values, not data. No poll influenced any of the three forecasts.

The locked records are unchanged and stay as the timestamped record, per this registry's append-only policy. Read them together with this disclosure.

## What the registry said, and what happened

| | What the registry published | What produced the locked forecasts |
| --- | --- | --- |
| Ensemble weights | "Composite-tuned": polls 0.20, fundamentals 0.22, expert 0.29, approval 0.68, sentiment 0.45, incumbency 1.00 | Hand-set weights: polls 0.38, fundamentals 0.22, sentiment 0.14, expert 0.16, live 0.10. The published set was never used to compute any forecast; it appears only as metadata written into the records. |
| Polls | Independent polls only | Weight 0. The prototype's polling input was off by default, so no poll entered any forecast. The Alabama record's note, "model still gives Marshall narrow lead on polling weight", is incorrect. |
| Fundamentals | Weight cut to 0.10 for primaries; approval removed | Simulated approval, unemployment, generic-ballot and incumbency values, generated from the text of the race ID. Effective weight about 0.40. |
| Expert ratings | Cook Political Report, Sabato's Crystal Ball, Inside Elections | A simulated rating generated from the race ID, displayed under those three raters' names. Effective weight about 0.32. |
| Sentiment | Not used (weight 0) | A simulated social-media baseline. Effective weight about 0.28. |
| Methodology version | Primaries locked from 2026-05-09 use `v1-primary-2026` | The records are stamped `v1-composite-tuned-2026-04-25`. None of the primary adjustments in `PRIMARY_METHODOLOGY.md` was applied. |
| Confidence interval | Widened 1.5× for primaries | ±5.40 pts is the unwidened 80% interval (1.2816 × σ 4.21). The 1.5× widening was recorded but not applied. |
| Validated baseline | 67.7% direction, 3.89 MAE, Brier 0.2373 on 65 races (in each record); 3.59 MAE, 72.3% direction, 90.9% governors (README) | Neither set can be reproduced from the retained backtest code and library. Both are withdrawn. |

## How this was established

Build v48.1 is retained. Loaded with its default settings, its own ensemble reproduces all three locked forecasts exactly:

| Race | Locked | Reproduced from v48.1 |
| --- | --- | --- |
| KY Senate (R) | Barr 64.1%, +1.30, ±5.40 | 64.1%, +1.30, 80% interval ±5.39 |
| AL Senate (R) | Marshall 55.6%, +0.89, ±5.40 | 55.6%, +0.89, 80% interval ±5.39 |
| GA Governor (R) | Jones 63.7%, +1.08, ±5.40 | 63.7%, +1.08, 80% interval ±5.40 |

In that build's source, the fundamentals input is labelled as simulated and is derived from a hash of the race ID. The expert rating is also a pseudo-random value derived from a hash of the race ID, although the code comment above it names Cook, Sabato and Inside Elections. The sentiment input is labelled as a hardcoded simulation baseline. The polling input is off unless switched on in the interface.

## What this means

- **These three forecasts are not evidence about any forecasting method.** Whatever the results were, they measure simulated inputs. They will not be reported as model validation, correct or incorrect.
- **The weights and baseline figures in `README.md` and `PRIMARY_METHODOLOGY.md` are superseded** by this disclosure. They describe a model that was never built.
- **The plan to lock November 2026 general-election forecasts under `v1-composite-tuned` is withdrawn.** Any future methodology will be published before its first lock, with its weights taken from the code that runs it.

Questions about this disclosure: Jonathan Epstein, PULSE INTEL.
