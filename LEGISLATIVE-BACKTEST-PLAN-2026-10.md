# Backtest plan · California floor votes, walk-forward

Written 2026-10-25, before any of the data below has been downloaded and before anything has been run. This file's commit date in this registry is the evidence that the plan, the baselines and the pass rules came first. It will not be edited once the first session's data is downloaded. If anything ever has to change, the change goes in a new dated file next to this one, it applies only to results not yet seen, and both are published.

Until a target passes under this plan, and that result is published here, the platform shows no probability, vote count or member call for any bill. The Call tab keeps saying "No forecast: not yet backtested."

## 1. Data

The source is the Legislature's own bulk export (Legislative Counsel, downloads.leginfo.legislature.ca.gov). Only closed sessions are used, each from the export the Legislature froze after the session ended. Before this file was committed, only HTTP HEAD requests had been made against these exports (2026-10-25):

| Session | Export | Bytes | Last-Modified | ETag |
|---|---|---|---|---|
| 2009–10 | `pubinfo_2009.zip` | 355,550,504 | Sat, 07 May 2011 03:53:18 GMT | `"15314528-4a2a78bf26780"` |
| 2011–12 | `pubinfo_2011.zip` | 511,365,005 | Sun, 25 Nov 2012 09:19:16 GMT | `"1e7acf8d-4cf4e4f8ecd00"` |
| 2013–14 | `pubinfo_2013.zip` | 514,835,580 | Mon, 01 Dec 2014 06:30:57 GMT | `"1eafc47c-50921c0d04a40"` |
| 2015–16 | `pubinfo_2015.zip` | 903,670,010 | Mon, 28 Nov 2016 05:51:36 GMT | `"35dce8fa-54256108f4a00"` |
| 2017–18 | `pubinfo_2017.zip` | 1,222,693,499 | Mon, 26 Nov 2018 05:27:05 GMT | `"48e0d27b-57b8a955a9c40"` |
| 2019–20 | `pubinfo_2019.zip` | 817,820,837 | Mon, 30 Nov 2020 05:26:09 GMT | `"30bef4a5-5b54c3f60be40"` |
| 2021–22 | `pubinfo_2021.zip` | 1,120,572,556 | Mon, 28 Nov 2022 05:27:40 GMT | `"42ca948c-5ee8121464b00"` |
| 2023–24 | `pubinfo_2023.zip` | 1,261,848,876 | Mon, 25 Nov 2024 05:26:38 GMT | `"4b36492c-627b5fa0d3f80"` |

- **Integrity.** An export whose ETag, size or Last-Modified differs from this table when it is downloaded is not used. The difference is published, and a new dated file decides what happens.
- **How the tables are read.** With HTTP Range requests, the same way as `data/fetch_ca_leginfo_bill.py` in the platform repository, checking every member's CRC-32.
- **Tables read in phase 1:**
  - `BILL_TBL` (bill identity only, see section 3), `BILL_HISTORY_TBL`, `BILL_VERSION_TBL` (metadata only, no texts), `BILL_VERSION_AUTHORS_TBL`
  - `BILL_SUMMARY_VOTE_TBL`, `BILL_DETAIL_VOTE_TBL`, `BILL_MOTION_TBL`, `LOCATION_CODE_TBL`, `LEGISLATOR_TBL`
- **Phase 1 reads no analysis text.** `BILL_ANALYSIS_TBL` and its Word files are read only in phase 2 (section 7).
- **What is committed.**
  - The extractor.
  - A derived dataset with one row per unit and one per member vote.
  - A manifest with each export's URL, Last-Modified, ETag and size, the CRC-32 of every member read, and the SHA-256 of every derived file.
  - The raw tables are not committed (`BILL_DETAIL_VOTE_TBL` alone runs to tens of MB per session). The manifest is enough to fetch them again and check them.
- **Party.** Each member's party comes from that session's own `LEGISLATOR_TBL`, as the export records it. The table records the session as it ended. Members who changed party are kept as recorded and listed in the result; they are not dropped or corrected by hand.
- **2025–26** is the live session and is not used for development or testing (section 8).

## 2. What is forecast

- **Unit: a floor passage attempt.** A bill, in one house, from the forecast point (section 3) in that house. A bill that reaches both floors is two units.
  - Concurrence votes are a separate kind of unit. They are scored and reported separately, and never pooled with third-reading units.
- **Target 1, passage.** Does the bill pass that house's floor by the end of the session?
  - Yes: a floor vote with result `(PASS)` on a third-reading motion in that house. The last such vote counts, so a bill that fails, is granted reconsideration and then passes has passed.
  - No: anything else by the end of the session. That includes failing, being moved to the inactive file and never voted on, being returned to committee, and dying on the third-reading file.
- **Target 2, tally.** The number of noes on the deciding floor vote: the last third-reading vote in that house. The aye share is also reported. Only units with a floor vote are scored.
- **Target 3, member votes.** Each member's recorded vote on the deciding floor vote: Aye, or not Aye (Noe, or no vote recorded). Noe is also reported on its own.
- **Base rates are not known yet.** Each session's base rates are computed from the data and published with the result.

### Sensitivity check, declared now

The passage result is also reported with one group of units excluded: bills moved to the inactive file in that house and never voted on there afterwards.
- How such a bill is identified: a history row in that house matching `/inactive file/i`, and no floor vote in that house dated after that row.
- The model and the baselines are scored on this reduced set with the same metrics and the same bootstrap.
- The number of units excluded is reported for each session.
- The sensitivity result is published beside the main result. It does not change the pass rule, which applies only to the main result with these bills counted as "not passed".

## 3. The forecast point, and what may be used at it

- **The forecast point.** The `ACTION_DATE` of the first history row ordering the bill to third reading in that house: "Ordered to third reading", "Read second time. Ordered to third reading.", or the export's equivalent wording. The extractor's list of matching phrasings is fixed in code before the test sessions are scored.
- **Allowed: only rows dated strictly before the forecast point.**
  - History actions.
  - Committee votes in this house.
  - For a second-house unit, the first house's floor votes.
  - Authors on the latest version dated before the point.
  - `VOTE_REQUIRED`, `URGENCY` and `TAXLEVY` on that version.
  - The party of each member, from `LEGISLATOR_TBL`.
  - Members' recorded votes before the point.
- **Never used:**
  - Any `BILL_TBL` field other than the bill's identity (`BILL_TBL` holds the state at the end of the session).
  - `LATEST_BILL_VERSION_ID`, `MEASURE_STATE`, any `CURRENT_*` field, chapter fields.
  - Any row dated on or after the forecast point.
- **Leakage test.** Each feature is computed by a function that receives the cutoff date and only the rows before it. A committed test adds rows dated after the point and checks that no feature changes.
- **Walk-forward across sessions.** Parameters for a test session are fitted only on the sessions before it.
  - **Training only:** 2009–10, 2011–12, 2013–14. Development and debugging use these three sessions alone.
  - **Test, in order:** 2015–16, 2017–18, 2019–20, 2021–22, 2023–24. Each is scored once, in one run, from the frozen commit (section 9).
- **Within a test session,** a member's record (for example, their earlier noes in that session) counts only from votes dated before the forecast point.

## 4. Baselines (fixed now)

- **B0, base rate.**
  - Passage: P(pass) = the pass rate of all units in the earlier sessions, by house.
  - Tally: the mean noes in the earlier sessions, by house.
  - Members: P(Aye) = the overall aye rate in the earlier sessions, by house.
- **B1, party line.**
  - Members: a member of the lead author's party votes Aye; every other member votes not Aye.
  - Tally: the number of members of that house not in the lead author's party.
  - Passage: the bill passes if the lead author's party holds at least the votes it needs in that house (a majority of the membership, or two-thirds when `VOTE_REQUIRED` says so).
- **B2, majority-party sponsor.**
  - Passage: P(pass) = the pass rate in the earlier sessions of units whose lead author is (or is not) in the house's majority party, by house.
  - Members: majority-party members P(Aye) = their party's aye rate in the earlier sessions on bills authored by that kind of member (majority or minority). Minority-party members likewise.
  - Tally: the sum of those probabilities, as a count of not-Aye.

**Probabilities from the deterministic baselines.** B1's forecasts are 0 or 1. For log loss only, every forecast (the model's and every baseline's) is clipped to [0.01, 0.99]. Brier score and MAE use the unclipped values.

**Which baseline the model must beat.** On each target, the model must beat the best of B0, B1 and B2 on that target's metric. For each session's comparison, the best is chosen on that session's scores; for the pooled comparison, on the pooled scores.

## 5. The phase 1 model (fixed before any test session is scored)

- **Method.** One logistic regression per target (passage; member Aye), with a fixed L2 penalty (C = 1.0) and features standardized on the training sessions. There is no model search and no tuning against test sessions.
- **Passage features:**
  - the lead author's party, and whether it is the house majority;
  - the share of coauthors from the other party;
  - the lowest aye share across this house's committee votes on the bill before the point;
  - the number of minority-party noes in those committee votes;
  - for a second-house unit, the first floor's aye share and minority-party noes;
  - two-thirds vote required, urgency and tax levy;
  - the number of committee referrals in this house;
  - the days from introduction to the forecast point.
- **Member features:**
  - the member's party, and whether it is the lead author's party;
  - the member's own vote on this bill in a committee of this house before the point (Aye, Noe, none recorded, not a member);
  - their party's aye share in those committee votes;
  - the member's noe rate on floor votes before the point (earlier sessions, then earlier in this session).
- **Tally.** The sum of the member probabilities of not-Aye. There is no separate tally model.
- **No analysis text in phase 1.** No feature reads `BILL_ANALYSIS_TBL` or any analysis file.

## 6. Scoring and the pass rule (phase 1)

- **Scoring.** Each test session is scored on its own and then pooled.
  - 95% confidence intervals come from a bootstrap of 2,000 resamples, with the seed fixed in the frozen code.
  - The bootstrap resamples bills. A bill's units and all member votes on its roll calls are resampled together.
- **Passage.**
  - Metrics: Brier score, log loss, reliability by decile.
  - Pass rule:
    - the pooled Brier skill score against the best baseline is at least **0.05**, and the 95% CI lower bound is above 0;
    - the model beats the best baseline in **at least 4 of the 5** test sessions;
    - calibration: in every decile that holds **at least 30 units** (pooled), the observed pass rate is within **0.05** of the mean forecast; pooled expected calibration error is at most **0.03**. Deciles with fewer than 30 units are reported but not scored.
- **Tally.**
  - Metric: mean absolute error in noes on the deciding vote.
  - Pass rule:
    - the pooled MAE is at least **10% lower** than the best baseline's, and the 95% CI of the difference excludes 0;
    - the model beats the best baseline in **at least 4 of 5** sessions;
    - the 80% interval (a Poisson-binomial from the member probabilities) covers **75–85%** of tallies, pooled.
- **Member votes.**
  - Metrics: log loss and Brier score for Aye against not Aye, and recall and precision on Noe.
  - Pass rule: the pooled log-loss skill against the best baseline is at least **0.05**, the CI lower bound is above 0, and the model beats the best baseline in **at least 4 of 5** sessions.
- **What a pass allows the platform to show.** Each target gates its own display:
  - a passage probability only if passage passes;
  - a vote count only if passage and tally both pass;
  - a member-by-member call only if all three pass.
  - A target that fails keeps "No forecast: not yet backtested" for what it covers.
- **Published whatever the outcome:**
  - **The baselines' own scores alongside the model's.** Every metric, CI and reliability table for each of B0, B1 and B2, for every target and every session, and pooled.
  - Which baseline was best in each session.
  - The number of units, units dropped and the reason for each.
  - The sensitivity check from section 2.
  - Members whose party changed.
  - The 2019–20 session (remote voting, a shortened calendar) is shown as it came out and is not removed afterwards.

## 7. Phase 2: registered opposition (declared now, run only after phase 1 is published)

Phase 2 asks whether the Legislature's analyses, read as the platform reads them, add anything. Its features, method and pass rule are fixed by this file now. They cannot be changed after phase 1's result is seen; a change is a new plan, scored only on sessions not yet scored.

- **Parser, frozen.** The registered-list rules of `data/fetch_ca_leginfo_bill.py` at platform commit `63eb9c2` (file SHA-256 `e1c54c54bf0ab6804f44b965a397101aa33a1d65eb8007fcd5166cb10463e29f`):
  - a list starts at "REGISTERED SUPPORT / OPPOSITION" (Assembly) or an upper-case position heading (Senate), and the opposition heading may be "Opposition" or "Oppose";
  - a list ends at the next section;
  - "None known", "None received" and "None on file" mark an empty list.
- **Data added.** `BILL_ANALYSIS_TBL` rows and their Word files, for analyses dated strictly before the forecast point, with the same manifest discipline as section 1.
- **Features added to phase 1's.** Taken from the latest analysis in this house dated before the point, or the first house's if this house has none:
  - the number of organizations registered in support and in opposition;
  - whether any opposition is listed;
  - whether any opposition is "oppose unless amended";
  - whether the analysis lists a sponsor.
  - Lines that count people ("41 Individuals") are not counted as organizations.
- **Method.** Identical to phase 1, refitted with the added features on the same training sessions, and scored on the same five test sessions with the same bootstrap and seed.
- **Coverage gate, before scoring.** On the training sessions alone, the share of units with an analysis before the point is reported. So is the share of those analyses where the parser finds a registered-list heading but reads no list. If that second share is above **5%**, phase 2 stops before any test session is scored, and that is published.
- **Pass rule (phase 2).** For each target where phase 1 passed, phase 2 is adopted only if it:
  - beats the **phase 1 model** with a pooled skill of at least **0.02** on that target's metric (Brier for passage, MAE reduction for tally, log loss for members), with the 95% CI lower bound above 0;
  - beats phase 1 in **at least 4 of 5** sessions;
  - still meets every phase 1 bar against the baselines.
  - For a target where phase 1 failed, phase 2 must meet that target's phase 1 bars against the baselines, unchanged.
- **Published either way,** with phase 1's and the baselines' scores beside it.

## 8. The live session and after

- 2025–26 is never scored retroactively.
- If a target passes, forecasts for 2027–28 floor votes are locked at each forecast point in this registry, as the election calls are, and scored as the votes happen.
- The bills now in the platform (AB 566, SB 7, AB 412 and SB 1130, all 2025–26) stay without a forecast.

## 9. Order of work

1. This file is committed and pushed. Until then nothing has been downloaded or run.
2. The extractor and the leakage tests are written and committed in the platform repository. The eight exports are downloaded and checked against section 1, and the manifest is committed.
3. Phase 1 is developed on 2009–10, 2011–12 and 2013–14 only. The frozen code is committed. A lock file in this registry records the code's commit hash and this file's SHA-256.
4. The five test sessions are scored in one run from that commit. The full output is published here with its SHA-256, pass or fail.
5. Phase 2, as declared in section 7, follows the same steps 2–4.
6. Only for a target that passes, a platform change that shows what that target allows is proposed and reviewed on its own.
