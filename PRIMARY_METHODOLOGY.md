# PULSE INTEL — Primary Forecast Methodology

**Version:** v1-primary-2026
**Effective:** 2026-04-26 (applies to all primaries locked May 9, 2026 onward)
**Companion to:** Composite-tuned general-election methodology (v1-composite-tuned)
**Status:** Active for 5 flagship primaries: KY-Senate-R (May 19), AL-Senate-R (May 19), CA-Governor (June 2), MI-Senate (Aug 4), MN-Senate (Aug 11)

---

## Purpose of this document

This is the public-facing methodology disclosure that accompanies every primary prediction PULSE INTEL locks to its registry. It must be linked from:

1. The README of the public registry repository
2. Each per-race file's `methodology_notes` field
3. Each lock_prediction.py git commit message (in summary form)

If a buyer, journalist, or peer reviewer asks "how did you forecast that primary?" — this document is the answer.

---

## The fundamental honesty

**PULSE INTEL's Composite-tuned ensemble was calibrated against 65 general elections (2016-2024).** Specifically: 22 presidential, 32 Senate, 11 gubernatorial. The model's coefficients (polls 0.20, fundamentals 0.22, expert 0.29, approval 0.68, sentiment 0.45, incumbency 1.00) were tuned to minimize MAE / Brier score / direction error against general-election outcomes.

**Primaries are out-of-distribution for this model.** Primary electorates are smaller, more ideological, more sensitive to endorsements and late breaking, and far less responsive to fundamentals (the in-party economic argument barely applies). Applying a model trained on generals to primaries is **a methodological stretch** — and we're being upfront about that.

We forecast primaries anyway because:

1. **Buyers need case studies.** Primary forecasts produce closed-loop validation in months, not years. We can deliver 5 case studies by August 11, 2026 — 6 months before any general-election validation is possible.
2. **The methodology is publicly testable in this regime.** If our model is too narrow to forecast primaries reliably, the locked predictions will reveal that — and we'll report the result honestly. That's stronger evidence of a credible methodology than a black-box claim of universal applicability.
3. **Most primary forecasts in the industry are unaccountable.** Campaign internals, partisan PAC polls, and unsystematic punditry dominate. PULSE INTEL's locked, public-registry approach is structurally more honest than what most political forecasting consultancies sell, even on a methodology that's a stretch.

---

## Adjustments applied for primary forecasts

The following adjustments are applied to the v1-composite-tuned model when forecasting a primary. Every adjustment is documented in the per-race file and the commit message.

### 1. Incumbency advantage: ZEROED

**Rationale:** Primaries are open contests within a party. The "incumbency advantage" coefficient (1.00 in generals) has no analog when no candidate is the incumbent.

**Implementation:** Set `incumbency_coeff = 0` for primary forecasts.

**Edge case:** If a sitting senator/governor is being primaried, that candidate's "incumbency" within the party may matter (institutional support, donor networks). Handled case-by-case in the per-race notes; default is still zero.

### 2. Sitting-president approval signal: REMOVED

**Rationale:** Approval of the sitting president matters in a general election (it shapes the in-party candidate's ceiling). In an in-party primary, it's irrelevant — every candidate is appealing to the same partisan base, and they all (mostly) align with the sitting president if same-party.

**Implementation:** `approval_coeff = 0` for primary forecasts; the approval signal is dropped from the ensemble for that race.

### 3. Endorsement signal: ELEVATED

**Rationale:** Primary voters are far more responsive to endorsements (especially from a popular party leader like Trump, in a GOP primary) than general-election voters. The expert ratings sub-model already captures this somewhat, but the primary-adjusted methodology elevates explicit endorsement signal.

**Implementation:** Each primary race forecast includes a manual `endorsement_modifier` field in the per-race file. Values: `+8`, `+5`, `+2`, `0`, `-2`, `-5` (in points of margin shift). Modifier is applied after the base ensemble runs and is fully transparent. Default is 0 unless a meaningful endorsement (party leader, state party chair, sitting senator) has occurred.

### 4. Confidence interval: WIDENED 1.5x

**Rationale:** Primary uncertainty is structurally higher than general-election uncertainty. Smaller polls, more late deciders, endorsement risk, lower turnout = wider error bars.

**Implementation:** Whatever confidence interval the model produces from polls/fundamentals/expert ratings is multiplied by 1.5x before being recorded as the locked CI.

**Example:** If model emits a base CI of ±4 points for a general election, primary lock CI is ±6 points.

### 5. Polls sub-model: ONLY INDEPENDENT POLLS

**Rationale:** Campaign internals and partisan PAC polls in primaries are heavily biased — pro-candidate-X internals show candidate X +14, while independent polls show a 5-point race. Including them in the ensemble corrupts the input.

**Implementation:** Only polls from independent academic and commercial pollsters (Pew, Quinnipiac, Marist, Marquette, AP-NORC, Emerson, Quantus, Co/efficient when not commissioned, Public Policy Polling, Trafalgar, InsiderAdvantage) feed into the polls sub-model. Campaign-commissioned and PAC-commissioned polls are excluded.

**Documentation:** Each primary's per-race file lists the specific polls used and excluded.

### 6. Fundamentals sub-model: REDUCED WEIGHT

**Rationale:** State-level economic indicators (unemployment, CPI, etc.) matter for general elections. They matter much less for primaries — voters in a party primary aren't blaming/crediting the in-party candidate for the state economy.

**Implementation:** `fundamentals_coeff` reduced from 0.22 to 0.10 for primary forecasts.

### 7. Expert ratings sub-model: UNCHANGED

**Rationale:** Cook, Sabato, and Inside Elections rate primaries the same way they rate generals — based on candidate quality, fundraising, polling, and historical patterns. Their ratings remain a useful signal.

**Implementation:** Expert coefficient unchanged at 0.29.

### 8. Sentiment sub-model: NOT USED

**Rationale:** Our sentiment infrastructure is sparse and not yet validated for primaries. Until we have a real social/news sentiment pipeline running, the sentiment signal is too noisy to include.

**Implementation:** `sentiment_coeff = 0` for primary forecasts.

---

## Resulting effective coefficients for primary forecasts

| Sub-model | General elections (v1-composite-tuned) | Primaries (v1-primary-2026) |
|-----------|----------------------------------------|------------------------------|
| Polls | 0.20 | 0.20 (independent only) |
| Fundamentals | 0.22 | 0.10 |
| Expert ratings | 0.29 | 0.29 |
| Approval (in-party) | 0.68 | 0.00 |
| Sentiment | 0.45 | 0.00 |
| Incumbency | 1.00 | 0.00 |
| Endorsement modifier | n/a | manual ±2 to ±8 pts |
| Confidence interval | base | base × 1.5 |

---

## What gets recorded in each per-race file

Every primary lock writes to `predictions/<race_id>.json` with these methodology fields:

```json
{
  "methodology_version": "v1-primary-2026",
  "methodology_notes": "Primary forecast — see PRIMARY_METHODOLOGY.md in registry root for full disclosure. Adjustments from v1-composite-tuned: incumbency=0, approval=0, sentiment=0, fundamentals 0.22→0.10, polls=independent-only, CI widened 1.5x.",
  "endorsement_modifier_pts": 0,
  "polls_included_count": 4,
  "polls_excluded_count": 5,
  "polls_excluded_reason": "Campaign-commissioned or PAC-commissioned (excluded for partisan bias)"
}
```

---

## Honesty obligations for case studies

When PULSE INTEL publishes a primary case study (e.g., "We called the KY Senate primary correctly, here's the analysis"), the case study MUST include:

1. **The methodology version used** (v1-primary-2026)
2. **A link to this document**
3. **The acknowledgment that this is an out-of-distribution application of the general-election model**
4. **The locked prediction's full record from the public registry**
5. **The actual result and the margin error**
6. **What the methodology got right or wrong, specifically**

Case studies that hide or downplay the methodological stretch are not permitted. We sell credibility, not certainty.

---

## What we do NOT claim about primary forecasts

- We do NOT claim primary forecasts have the same accuracy profile as the 65-race general-election backtest (3.59 MAE / 72.3% direction)
- We do NOT claim the Composite-tuned coefficients are validated for primary use (they're not; they were tuned on generals)
- We do NOT claim primary uncertainty is well-calibrated (the 1.5x CI widening is a heuristic, not a measurement)

These claims will become defensible only after multiple primary cycles produce enough closed-loop case studies to backtest a primary-specific tune. Earliest that work could begin: 2027, after 2026 primaries resolve.

---

## What primary case studies WILL demonstrate

Even with the methodology caveats above, a clean run of primary forecasts demonstrates:

1. **Operational discipline.** PULSE INTEL locks predictions publicly, on a schedule, with timestamps. No post-hoc adjustments.
2. **Methodology transparency.** Every assumption is documented. Buyers can replicate or challenge any input.
3. **Calibrated humility.** When a forecast is wrong, the registry shows by how much, and the methodology disclosure explains why uncertainty was higher to begin with.
4. **Closed-loop accountability.** Predictions are recorded, then resolved with actuals via record_actual.py. Public git history is the audit trail.

These four properties are what differentiate PULSE INTEL from punditry. They hold whether the forecast is right or wrong on any given race.

---

## Document changelog

- **2026-04-26 v1-primary-2026:** Initial publication. Authored alongside KY Senate GOP primary brief preparation.

---

*This document is a living methodology disclosure. Updates will be tracked in this changelog and announced via the registry README.*
