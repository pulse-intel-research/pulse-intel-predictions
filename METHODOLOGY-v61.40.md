# Methodology v61.40 — November 2026 general-election forecasts

**Method: recency-weighted polling average with historical-error intervals.**

Locked 2026-10-08T03:40:41.902Z. Forecast as-of date 2026-10-07. Build `pulse-intel-v6140.html`, SHA-256 `acca933752b328c06803ae6afd3615c731e134c6f949a328654bbb50ba5b7bb6`.

Every number in the lock records below is computed by `ensemblePredict()` in that build, from the input files listed at the end, and can be recomputed by loading the build and calling `ensemblePredict(race_id)`. Nothing in the forecast path reads the clock.

## Validation caveat

**These forecasts are not validated by the platform's 73-race backtest.** That backtest ran a different configuration — a multi-input ensemble with fundamentals, sentiment, expert ratings and momentum, a positional recency decay, and no σ floor of this kind — on 2016–2024 races. It does not validate these calls. The σ floor (4.67) is the historical error of a simple polling average on 730 Senate and Governor generals (1998–2022); it is a floor on uncertainty, not a measure of this method's accuracy.

**Addendum, 2026-10-08:** [walk-forward backtest of this method](METHODOLOGY-v61.40-addendum-2026-10-08.md) on those 730 races. Its 80% and 95% intervals held the actual result 70.8% and 88.9% of the time the day before the election. The lock records below are unchanged and will be scored as locked; their intervals are expected to be too narrow.

## The method

- **Input:** polls only (VoteHub, vintage 2026-10-07T02:42:11.186898Z). Partisan-sponsored and internal polls are excluded; one row is kept per fielding (LV preferred); a poll must give a number for both principal candidates.
- **Average:** each poll's weight = 0.5^(age_days / 30) × 538 weight, with age measured from the poll's end date to 2026-10-07. The 538 weight = clip(1 - (POLLSCORE + 1) / 3, 0.1, 1), rounded to 0.01; letter-grade fallback when POLLSCORE is absent, from the archived 538 ratings (hashes below); unrated pollsters get 1.0. No house-effect correction, no pollster-quality multiplier. Polls are summed in a fixed order, so input order cannot change the result.
- **Margin:** the weighted average share of c0 minus that of c1.
- **σ:** poll σ = max(1.8, 0.7 × recency-weighted mean MoE), with MoE = 98/√n. Final σ = max(poll σ, 4.67), the floor being the historical polling-average error above.
- **The floor binds in every locked race.** Poll σ is between 2.04 and 2.59, below 4.67 in all 11, so σ = 4.67 for every race and **win probability = Φ(margin / 4.67)**, Φ by Abramowitz–Stegun 26.2.17, no clamp.
- **Intervals:** margin ± 1.282 × 4.67 (80%) and margin ± 1.96 × 4.67 (95%).
- **Lock eligibility:** at least 8 polls after exclusions and the newest poll ending within 45 days of 2026-10-07; in me-sen-gen, every poll must report exactly two answers (head-to-head or a ranked-choice final round).

## Inputs not used

- **fundamentals:** Not used: the fundamentals coefficients are hand-set and were never validated, and the sub-model has no state partisan-lean term, so it applies the same national shift to every race. Its inputs (FRED unemployment, approval, generic ballot) are archived as collected, not used.
- **expert:** Not used: no expert ratings are held for 2026 general elections.
- **sentiment:** Not used: no live sentiment feed exists; the platform's sentiment values are simulated.
- **live:** Not used: no SMS poll data.
- **momentum:** disabled. **calibration correction:** not applied.

### Collected, not used

These were gathered for the fundamentals input and are archived with hashes (below), but do not enter any forecast: presidential approval 35% and generic ballot D+7.7 (FiftyPlusOne, 2026-10-06, from saved copies of the pages); FRED unemployment (data/fred_snapshot.json); incumbency per race. Spread across aggregators on 2026-10-06: approval 35–37.3, generic ballot D+7.7 to D+9.6.

## Locked forecasts

| Race | Predicted winner | Margin (pts) | Win prob. | σ | 80% interval | 95% interval | Polls (raw n / effective n) | Newest poll |
|---|---|---|---|---|---|---|---|---|
| Michigan Senate 2026 — general election | Abdul El-Sayed | 2.90 | 73.3% | 4.67 | -3.09 to 8.89 | -6.25 to 12.05 | 21 / 13.42 | 2026-10-01 |
| North Carolina Senate 2026 — general election | Roy Cooper | 9.66 | 98.1% | 4.67 | 3.67 to 15.65 | 0.51 to 18.81 | 21 / 10.66 | 2026-09-29 |
| Ohio Senate 2026 — general election | Sherrod Brown | 3.86 | 79.6% | 4.67 | -9.85 to 2.13 | -13.01 to 5.29 | 14 / 6.95 | 2026-09-29 |
| Iowa Senate 2026 — general election | Josh Turek | 1.49 | 62.5% | 4.67 | -7.48 to 4.5 | -10.64 to 7.66 | 10 / 5.89 | 2026-09-28 |
| Texas Senate 2026 — general election | James Talarico | 2.74 | 72.1% | 4.67 | -8.73 to 3.25 | -11.89 to 6.41 | 27 / 14.42 | 2026-09-28 |
| New Hampshire Senate 2026 — general election | Chris Pappas | 5.52 | 88.1% | 4.67 | -11.51 to 0.47 | -14.67 to 3.63 | 12 / 5.21 | 2026-09-22 |
| Iowa Governor 2026 — general election | Rob Sand | 8.30 | 96.2% | 4.67 | -14.29 to -2.31 | -17.45 to 0.85 | 11 / 7.47 | 2026-10-01 |
| Florida Governor 2026 — general election | Byron Donalds | 2.69 | 71.8% | 4.67 | -3.3 to 8.68 | -6.46 to 11.84 | 13 / 5.48 | 2026-09-27 |
| Georgia Senate 2026 — general election | Jon Ossoff | 9.32 | 97.7% | 4.67 | 3.33 to 15.31 | 0.17 to 18.47 | 9 / 4.19 | 2026-10-03 |
| Georgia Governor 2026 — general election | Rick Jackson | 0.88 | 57.5% | 4.67 | -5.11 to 6.87 | -8.27 to 10.03 | 9 / 4.78 | 2026-10-03 |
| Maine Senate 2026 — general election | Troy Jackson | 2.22 | 68.3% | 4.67 | -8.21 to 3.77 | -11.37 to 6.93 | 11 / 9.61 | 2026-10-04 |

Margins and intervals are c0 minus c1 as listed in each record (positive favours c0).

## Polls per race

| Race | In snapshot | Partisan/internal excluded | Duplicate population dropped | Used | Effective n | Poll σ |
|---|---|---|---|---|---|---|
| mi-sen-gen | 31 | 9 | 1 | 21 | 13.42 | 2.54 |
| nc-sen-gen | 29 | 5 | 3 | 21 | 10.66 | 2.59 |
| oh-sen-gen | 15 | 1 | 0 | 14 | 6.95 | 2.25 |
| ia-sen-gen | 15 | 4 | 1 | 10 | 5.89 | 2.25 |
| tx-sen-gen | 32 | 5 | 0 | 27 | 14.42 | 2.2 |
| nh-sen-gen | 12 | 0 | 0 | 12 | 5.21 | 2.04 |
| ia-gov-gen | 15 | 3 | 1 | 11 | 7.47 | 2.4 |
| fl-gov-gen | 14 | 1 | 0 | 13 | 5.48 | 2.21 |
| ga-sen-gen | 9 | 0 | 0 | 9 | 4.19 | 2.45 |
| ga-gov-gen | 10 | 1 | 0 | 9 | 4.78 | 2.45 |
| me-sen-gen | 12 | 1 | 0 | 11 | 9.61 | 2.35 |

## Tracked, not locked

| Race | Reason |
|---|---|
| az-gov-gen | newest poll 2026-08-19 is 49 days old > 45 |
| wi-gov-gen | 4 polls < 8 |
| nv-gov-gen | 3 polls < 8 |
| mn-sen-gen | 5 polls < 8 |
| mn-gov-gen | 5 polls < 8 |

Alaska Senate has no forecast: VoteHub cannot attribute polls between the two candidates named Dan Sullivan, so there are no usable polls.

## Input files

| File | Role | SHA-256 |
|---|---|---|
| `pulse-intel-v6140.html` | build | `acca933752b328c06803ae6afd3615c731e134c6f949a328654bbb50ba5b7bb6` |
| `data/votehub_raw/2026-10-07T024211/MANIFEST.json` | VoteHub raw-response manifest | `3a229c1f84ab11f325912c5cb3901cc77eb377ddfea9b876fa75d9daf5169f2a` |
| `data/votehub_raw/2026-10-07T024211/mi-sen-gen.json` | VoteHub raw /polls response, mi-sen-gen | `91848a5bfcc7512751bcdc45e16a1f9d19d0fb9bca21bdded6dac37f27aa45e0` |
| `data/votehub_raw/2026-10-07T024211/me-sen-gen.json` | VoteHub raw /polls response, me-sen-gen | `912748385c9ccfb4b21394477dc236b48240ed48d50c415297ab9d3c5174ee14` |
| `data/votehub_raw/2026-10-07T024211/nc-sen-gen.json` | VoteHub raw /polls response, nc-sen-gen | `a363486742764cb9f05dd6c29fd36072bfb3024b3400c62e8c2eee3b1f66cb2f` |
| `data/votehub_raw/2026-10-07T024211/oh-sen-gen.json` | VoteHub raw /polls response, oh-sen-gen | `587ef091ced1c7a43df7af03208a7c11e2c9d11d8a482de10b3709d55e139922` |
| `data/votehub_raw/2026-10-07T024211/ga-sen-gen.json` | VoteHub raw /polls response, ga-sen-gen | `447a0b756473ca855728618a1af2156a5dcd22b9e216175ec539156a5cb3a549` |
| `data/votehub_raw/2026-10-07T024211/ia-sen-gen.json` | VoteHub raw /polls response, ia-sen-gen | `25cd815be0bf45396ebe6dc1eb75b3c58ad86b0adee93b516fcf723169918114` |
| `data/votehub_raw/2026-10-07T024211/tx-sen-gen.json` | VoteHub raw /polls response, tx-sen-gen | `1a2da83b5a32606e9292fe17e966f964bb3895ea895d936fdc675e7a59b7eb24` |
| `data/votehub_raw/2026-10-07T024211/nh-sen-gen.json` | VoteHub raw /polls response, nh-sen-gen | `fd6ce1a95163d335595093f4b9e151914f036bc306df62c0c14327dd4e19820d` |
| `data/votehub_raw/2026-10-07T024211/mn-sen-gen.json` | VoteHub raw /polls response, mn-sen-gen | `9101ace618d38a0a57a1f4b89a9bb2c653f970893c577deb409d3bd443ff0268` |
| `data/votehub_raw/2026-10-07T024211/az-gov-gen.json` | VoteHub raw /polls response, az-gov-gen | `944d1c1cf13b6ac9ce4af7deb97f5f4462742c1b953adab337ad2c9d09b0b054` |
| `data/votehub_raw/2026-10-07T024211/mi-gov-gen.json` | VoteHub raw /polls response, mi-gov-gen | `f07f8c09ad280cfba6f24358e5a604aebdda619c3e7b3cc045dd02a853a3d219` |
| `data/votehub_raw/2026-10-07T024211/nv-gov-gen.json` | VoteHub raw /polls response, nv-gov-gen | `805e42ae0161fc2d8ce1da544f77691b110df9d4c037bd9857badf56c3a92b0a` |
| `data/votehub_raw/2026-10-07T024211/wi-gov-gen.json` | VoteHub raw /polls response, wi-gov-gen | `61b54f4b701568cf5ba974c986ed4e74123c6aa0d98fc5562da9eed22da24646` |
| `data/votehub_raw/2026-10-07T024211/ia-gov-gen.json` | VoteHub raw /polls response, ia-gov-gen | `eb1cee1f7a672ced577265968a863b67e081cbe090d63ea2ab7a297eec776d0e` |
| `data/votehub_raw/2026-10-07T024211/ga-gov-gen.json` | VoteHub raw /polls response, ga-gov-gen | `094bd40021f40eff37ebd1ccf3fe715d63dcf726e7f3fdb4cde80c1b0722c929` |
| `data/votehub_raw/2026-10-07T024211/ks-gov-gen.json` | VoteHub raw /polls response, ks-gov-gen | `830f0a5a6f3b39177de6155e356fbdd02f9becf218f8ba95361696cadc22fa9e` |
| `data/votehub_raw/2026-10-07T024211/me-gov-gen.json` | VoteHub raw /polls response, me-gov-gen | `2064bbda5511b8582e662969e8d22ab2642749091318f00d3d415115e6bd9460` |
| `data/votehub_raw/2026-10-07T024211/fl-gov-gen.json` | VoteHub raw /polls response, fl-gov-gen | `bb39eea2b618ddd48cc31855d8c755bdc36dc699d39034383cb10a92a8027799` |
| `data/votehub_raw/2026-10-07T024211/mn-gov-gen.json` | VoteHub raw /polls response, mn-gov-gen | `bc3ea8f5998efe46bb9762dca4696d01de5b643034d941f052b30c6dec978e8f` |
| `votehub_polls.json` | VoteHub processed snapshot | `2ec480b08eed887ca39441cd55b35c904c1443b67e3a09cc0f1d900a11dba097` |
| `data/fred_snapshot.json` | FRED snapshot | `5432c338fc64229692e37ce5bbaac24c671f0bddd6f86ea02970eb091a2a2e69` |
| `data/political_snapshots/2026-10-06/MANIFEST.json` | political snapshots manifest | `d2155cbbededfe811e2b01b00dd561923d5d73d5f7defba77834db54af973f17` |
| `data/political_snapshots/2026-10-06/fiftyplusone-approval-president.html` | saved aggregator page (trump_approval_national) | `b228ce8f2525d8fca1d707423b461b4eeb9d61bb6ec80aca6c3bf22fa0ce9bb6` |
| `data/political_snapshots/2026-10-06/fiftyplusone-generic-ballot.html` | saved aggregator page (generic_ballot) | `28d1d21d831ed4e6770ccb4c5af48f3ff500a8b8cb57fd70a9d57c85131b5024` |
| `data/538/pollster-ratings__pollster-ratings-combined.csv` | 538 pollster ratings (POLLSCORE) | `75215795f59d6dd9c725c794b2222db140048aff27510847d1c5b145af3c04ef` |
| `data/538/pollster-ratings__2023__pollster-ratings.csv` | 538 pollster ratings (letter grades) | `8501615e7bff043dd3ed0452b875a93f519cec546c190a5d0a462272c387d923` |

## predState defaults

```json
{
  "pollingEnabled": true,
  "pollRecency": 3,
  "pollWeight": 35,
  "activePollSources": [
    "DataEdge",
    "eco",
    "emerson",
    "fox",
    "nyt",
    "quin",
    "rcp",
    "votehub"
  ]
}
```
