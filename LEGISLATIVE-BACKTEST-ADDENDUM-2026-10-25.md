# Addendum to the legislative backtest plan · 2026-10-25

This file goes next to `LEGISLATIVE-BACKTEST-PLAN-2026-10.md` (registry commit `d5176e9`). It was written and committed before any test session's data was downloaded, loaded or scored. When this file was committed:
- only the three training sessions (2009–10, 2011–12, 2013–14) had been downloaded;
- none of 2015–16, 2017–18, 2019–20, 2021–22 or 2023–24 had been read beyond its zip's central directory (the list of files in the zip), which holds no rows.

Section 1 of this file changes one rule of the plan. Section 2 writes down definitions the plan left to the extractor. Every threshold in the plan is unchanged.

## 1. The tally target is the count of members not voting Aye

**The contradiction.** The plan is inconsistent about the tally:
- Section 2 scores it as "the number of noes on the deciding floor vote".
- Section 5 forecasts it as "the sum of the member probabilities of not-Aye".
- Section 4's baselines also forecast not-Aye counts: B1 counts every member outside the lead author's party, and B2 sums the members' probabilities of not voting Aye.
- "Not Aye" is a Noe or no vote recorded (Target 3). So the plan forecasts one quantity and scores another.

**How it was found.** It was found on the training session 2013–14 only, during development (model fitted on 2009–10 and 2011–12). No test session was loaded or scored.
- On 2013–14, roll calls averaged 6.1 noes but 10.3 members not voting Aye.
- The model's mean forecast was 11.1, and its 80% interval held the recorded noes on only 20% of roll calls.
- Scored as written, the tally would fail because of the definition, whatever the forecasts were worth.

**The change.** The tally target is the number of members of that house **not voting Aye** on the deciding roll call: Noes plus members with no vote recorded, counted from the roll call's member rows.
- B0's tally becomes the mean not-Aye count by house in the earlier sessions.
- The model, B1 and B2 are unchanged; they already forecast this count.
- The 80% interval is scored against the same count.
- Every threshold is unchanged: MAE at least 10% lower than the best baseline's, CI of the difference excluding 0, at least 4 of 5 sessions, and 80% coverage between 75% and 85%.
- The MAE of the same forecasts against the recorded noes is still reported, but it is not part of the pass rule.

**Why not-Aye is the right target in California.** A bill passes a house only with the votes of a majority of that house's full membership (Constitution, Art. IV, §8(b)), or two-thirds of it where required: 41 of 80 in the Assembly, 21 of 40 in the Senate. A majority of those voting is not enough. So a member who does not vote counts against the bill exactly as a Noe does. What decides passage is how many members vote Aye, and how many do not.

## 2. Definitions the plan leaves to the extractor

These are fixed in `backtest/extract.py` at platform commit `4a721f0` (pulse-intel-research/pulse-intel-prototype), written on the training sessions only.

**Units and the forecast point**
- **Bills.** Measures of type AB and SB, in the regular session and in any extraordinary session.
- **Third-reading units.** A unit's forecast point is the first history row in that house matching `/\b(ordered )?to third reading\b/i`.
  - That covers "Read second time. Ordered to third reading." (2011 on), "Read second time.  To third reading." (2009–10) and their amended forms.
  - The house of a history row is its `PRIMARY_LOCATION`.
  - Bills sent straight to the consent calendar are never ordered to third reading, so they are not units. This follows from the plan's definition of the forecast point.
- **Concurrence units.** The forecast point is the first history row matching "Concurrence in … amendments pending" or "Concurrence pending", in the house of origin. They are fitted and scored separately and have no pass rule.

**Votes and outcomes**
- **Passage votes.** A floor vote is a passage vote when its motion text matches `/\b(third|3rd)\s+reading\b|consent calendar|special consent/i` and not `/reconsider|urgency|amend|concurr/i`.
  - Consent-calendar votes pass bills on third reading.
  - Urgency-clause, reconsideration and amendment votes are not passage votes.
  - A concurrence vote matches `/concurr/i`.
- **Outcome and deciding vote.** The deciding vote is the last passage vote in that house dated on or after the forecast point; the unit passed if that vote's result is `(PASS)`. A unit with no such vote did not pass.
- **Motion text for 2009–10.** The 2009–10 export has no `BILL_MOTION_TBL`. The motion table is cumulative, and the 2011–12 export's table (pinned in the plan) holds every 2009–10 motion ID but one. That one floor vote has no motion text and counts as neither a passage nor a concurrence vote.
- **Members on a roll call.** Every member row of the deciding vote (AYE, NOE and ABS rows).

**Authors and party**
- **Lead author.** The `LEAD_AUTHOR` of the latest version dated before the point, with `PRIMARY_AUTHOR_FLG = Y` first.
  - A committee author's party is "committee". It holds no seats under B1, and no member shares it.
- **Party.** Looked up by house and name in that session's `LEGISLATOR_TBL`, or by name alone when that is unique.
- **Seats for B1.** Counted from the `LEGISLATOR_TBL` rows of that house, which can include members who left during the session.

**Feature encoding**
- The lead author's party is two indicators (Democrat, Republican).
- A unit with no committee vote before the point has a lowest committee aye share of 1.0 and no minority-party noes.
- A member whose party cast no committee votes on the bill has a party aye share of 1.0.
- The first-floor features are 0 for a first-house unit, with an indicator for second-house (and concurrence) units.
- A member with no floor record before the point has a noe rate of −1, with an indicator.
- A member's own committee vote is three indicators (Aye, Noe, no vote recorded), against "not on a committee that voted".
- A member's floor record is keyed by the name on the vote rows, across sessions and houses.

**Scoring**
- **Best baseline.** The baseline with the best score on that target: per session for the per-session comparisons, and pooled for the pooled comparison.
- **Reliability.** Ten bins of width 0.1 on the forecast probability.
- **Bootstrap.** 2,000 resamples of bills within each session, seed 20261025.
- **Noe prediction.** For the Noe recall and precision that are reported, a member is predicted not to vote Aye when P(Aye) < 0.5.
