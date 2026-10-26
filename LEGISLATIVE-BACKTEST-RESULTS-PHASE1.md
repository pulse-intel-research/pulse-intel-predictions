# Backtest results · phase 1 · California floor votes, walk-forward

Run under `LEGISLATIVE-BACKTEST-PLAN-2026-10.md` and `LEGISLATIVE-BACKTEST-ADDENDUM-2026-10-25.md`, from the frozen commit recorded in `LEGISLATIVE-BACKTEST-LOCK-PHASE1.json`. Each test session was forecast from a fit on the sessions before it only, and scored once. The full output is `LEGISLATIVE-BACKTEST-RESULTS-PHASE1.json`, SHA-256 `3f385f91f681e080ab5669227709347df0eb8f540a30247a84c3b08acf4bcdbe`.

## Pass or fail

| Target | Result | Rules |
|---|---|---|
| Passage | **FAIL** | beats_4_of_5: met; ci_lower_gt_0: met; deciles_within_0.05: **not met**; ece_le_0.03: met; skill_ge_0.05: met |
| Tally (not-Aye count) | **FAIL** | beats_4_of_5: met; diff_ci_excludes_0: met; interval80_covers_75_85: **not met**; mae_reduction_ge_10pct: met |
| Member votes | **PASS** | beats_4_of_5: met; ci_lower_gt_0: met; skill_ge_0.05: met |

What this allows the platform to show (plan, section 6): a passage probability: **no**; a vote count: **no**; member-by-member calls: **no**. Nothing changes in the platform until this result has been reviewed.

## Passage (third reading, each house)

### Brier score (lower is better)

| Session | n | Model | B0 base rate | B1 party line | B2 majority-party sponsor | Best baseline | Model beats it | Skill |
|---|---|---|---|---|---|---|---|---|
| 2015–16 | 3862 | 0.0615 | 0.0923 | 0.2491 | 0.0919 | B2 majority-party sponsor | yes | 0.331 |
| 2017–18 | 4156 | 0.0627 | 0.0898 | 0.2264 | 0.0894 | B2 majority-party sponsor | yes | 0.299 |
| 2019–20 | 3181 | 0.0542 | 0.0859 | 0.2248 | 0.0859 | B0 base rate | yes | 0.368 |
| 2021–22 | 4157 | 0.0565 | 0.0958 | 0.2249 | 0.0951 | B2 majority-party sponsor | yes | 0.406 |
| 2023–24 | 4505 | 0.0443 | 0.0755 | 0.2166 | 0.0750 | B2 majority-party sponsor | yes | 0.409 |
| **Pooled** | 19861 | 0.0556 | 0.0877 | 0.2280 | 0.0873 | B2 majority-party sponsor | 5 of 5 | 0.362 (95% CI 0.339 to 0.385) |

Pooled 95% intervals (Brier): Model 0.0532 to 0.0583; B0 base rate 0.0843 to 0.0911; B1 party line 0.2213 to 0.2350; B2 majority-party sponsor 0.0838 to 0.0908.

### Log loss (forecasts clipped to [0.01, 0.99])

| Session | n | Model | B0 base rate | B1 party line | B2 majority-party sponsor | Best baseline | Model beats it | Skill |
|---|---|---|---|---|---|---|---|---|
| 2015–16 | 3862 | 0.2292 | 0.3312 | 1.1547 | 0.3296 | B2 majority-party sponsor | yes | 0.304 |
| 2017–18 | 4156 | 0.2297 | 0.3248 | 1.0505 | 0.3229 | B2 majority-party sponsor | yes | 0.289 |
| 2019–20 | 3181 | 0.2059 | 0.3145 | 1.0429 | 0.3143 | B2 majority-party sponsor | yes | 0.345 |
| 2021–22 | 4157 | 0.2178 | 0.3409 | 1.0436 | 0.3378 | B2 majority-party sponsor | yes | 0.355 |
| 2023–24 | 4505 | 0.1774 | 0.2864 | 1.0056 | 0.2835 | B2 majority-party sponsor | yes | 0.374 |
| **Pooled** | 19861 | 0.2114 | 0.3191 | 1.0579 | 0.3170 | B2 majority-party sponsor | 5 of 5 | 0.333 (95% CI 0.313 to 0.352) |

Pooled 95% intervals (log loss): Model 0.2036 to 0.2196; B0 base rate 0.3100 to 0.3284; B1 party line 1.0268 to 1.0898; B2 majority-party sponsor 0.3077 to 0.3264.

### Reliability, pooled (bins of width 0.1; scored only with at least 30 units)

| Forecast bin | Model (n · forecast · observed) | B0 base rate (n · forecast · observed) | B1 party line (n · forecast · observed) | B2 majority-party sponsor (n · forecast · observed) |
|---|---|---|---|---|
| 0.0–0.1 | 153 · 0.080 · 0.242 | — | 3709 · 0.000 · 0.851 | — |
| 0.1–0.2 | 343 · 0.139 · 0.052 | — | — | — |
| 0.2–0.3 | 156 · 0.263 · 0.212 | — | — | — |
| 0.3–0.4 | 458 · 0.351 · 0.321 | — | — | — |
| 0.4–0.5 | 268 · 0.437 · 0.493 | — | — | — |
| 0.5–0.6 | 119 · 0.551 · 0.765 | — | — | — |
| 0.6–0.7 | 149 · 0.645 · 0.906 | — | — | — |
| 0.7–0.8 | 102 · 0.764 · 0.755 | — | — | — |
| 0.8–0.9 | 2158 · 0.875 · 0.890 | 12039 · 0.874 · 0.898 | — | 11867 · 0.869 · 0.892 |
| 0.9–1.0 | 15955 · 0.954 · 0.962 | 7822 · 0.904 · 0.912 | 16152 · 1.000 · 0.915 | 7994 · 0.914 · 0.920 |
| ECE | 0.0163 | 0.0174 | 0.2280 | 0.0160 |

### Sensitivity check: excluding bills moved to the inactive file and never voted on (not part of the pass rule)

Excluded: 2015–16 157, 2017–18 175, 2019–20 94, 2021–22 161, 2023–24 105.

| Session | n | Model | B0 base rate | B1 party line | B2 majority-party sponsor | Best baseline | Model beats it | Skill |
|---|---|---|---|---|---|---|---|---|
| 2015–16 | 3705 | 0.0410 | 0.0668 | 0.2332 | 0.0669 | B0 base rate | yes | 0.387 |
| 2017–18 | 3981 | 0.0387 | 0.0610 | 0.2067 | 0.0610 | B2 majority-party sponsor | yes | 0.365 |
| 2019–20 | 3087 | 0.0362 | 0.0677 | 0.2076 | 0.0674 | B2 majority-party sponsor | yes | 0.464 |
| 2021–22 | 3996 | 0.0311 | 0.0693 | 0.2012 | 0.0684 | B2 majority-party sponsor | yes | 0.546 |
| 2023–24 | 4400 | 0.0281 | 0.0590 | 0.2011 | 0.0582 | B2 majority-party sponsor | yes | 0.517 |
| **Pooled** | 19169 | 0.0347 | 0.0645 | 0.2096 | 0.0641 | B2 majority-party sponsor | 5 of 5 | 0.458 (95% CI 0.430 to 0.484) |

Pooled 95% intervals (Brier): Model 0.0328 to 0.0367; B0 base rate 0.0614 to 0.0676; B1 party line 0.2027 to 0.2164; B2 majority-party sponsor 0.0610 to 0.0673.


| Forecast bin | Model (n · forecast · observed) | B0 base rate (n · forecast · observed) | B1 party line (n · forecast · observed) | B2 majority-party sponsor (n · forecast · observed) |
|---|---|---|---|---|
| 0.0–0.1 | 148 · 0.080 · 0.250 | — | 3555 · 0.000 · 0.886 | — |
| 0.1–0.2 | 328 · 0.139 · 0.055 | — | — | — |
| 0.2–0.3 | 119 · 0.263 · 0.277 | — | — | — |
| 0.3–0.4 | 409 · 0.352 · 0.357 | — | — | — |
| 0.4–0.5 | 245 · 0.436 · 0.539 | — | — | — |
| 0.5–0.6 | 106 · 0.552 · 0.849 | — | — | — |
| 0.6–0.7 | 140 · 0.644 · 0.964 | — | — | — |
| 0.7–0.8 | 87 · 0.762 · 0.885 | — | — | — |
| 0.8–0.9 | 2014 · 0.875 · 0.953 | 11577 · 0.874 · 0.931 | — | 11405 · 0.869 · 0.925 |
| 0.9–1.0 | 15573 · 0.954 · 0.983 | 7592 · 0.904 · 0.938 | 15614 · 1.000 · 0.944 | 7764 · 0.914 · 0.945 |
| ECE | 0.0406 | 0.0476 | 0.2096 | 0.0461 |

## Tally: members not voting Aye on the deciding roll call

### Mean absolute error (lower is better)

| Session | n | Model | B0 base rate | B1 party line | B2 majority-party sponsor | Best baseline | Model beats it | Skill |
|---|---|---|---|---|---|---|---|---|
| 2015–16 | 3500 | 5.442 | 9.244 | 17.856 | 9.289 | B0 base rate | yes | 0.411 |
| 2017–18 | 3777 | 4.895 | 8.626 | 16.062 | 8.517 | B2 majority-party sponsor | yes | 0.425 |
| 2019–20 | 2892 | 4.542 | 7.666 | 14.774 | 7.203 | B2 majority-party sponsor | yes | 0.369 |
| 2021–22 | 3737 | 4.399 | 7.273 | 14.414 | 6.960 | B2 majority-party sponsor | yes | 0.368 |
| 2023–24 | 4149 | 4.060 | 6.522 | 13.966 | 6.193 | B2 majority-party sponsor | yes | 0.344 |
| **Pooled** | 18055 | 4.650 | 7.829 | 15.381 | 7.600 | B2 majority-party sponsor | 5 of 5 | 0.388 (95% CI 0.382 to 0.394) |

Pooled 95% intervals (MAE): Model 4.590 to 4.709; B0 base rate 7.763 to 7.894; B1 party line 15.113 to 15.636; B2 majority-party sponsor 7.533 to 7.670.

80% interval (Poisson-binomial over the members): pooled coverage 0.383 over 18055 roll calls; by session 2015–16 0.298, 2017–18 0.373, 2019–20 0.330, 2021–22 0.439, 2023–24 0.449.

Mean per roll call: 2015–16: not-Aye 8.89, noes 6.40, model 11.22, B0 12.19, B1 25.74, B2 12.44; 2017–18: not-Aye 9.32, noes 6.01, model 10.18, B0 11.46, B1 23.64, B2 11.02; 2019–20: not-Aye 8.23, noes 4.28, model 8.06, B0 11.09, B1 20.54, B2 9.09; 2021–22: not-Aye 8.88, noes 4.09, model 8.29, B0 10.69, B1 20.77, B2 8.99; 2023–24: not-Aye 8.13, noes 3.36, model 7.89, B0 10.38, B1 20.11, B2 8.59.

Reported, not gated (addendum): the same forecasts against recorded **noes**, MAE pooled: B0 base rate 8.452, B1 party line 17.591, B2 majority-party sponsor 7.869, Model 5.535.

## Member votes (Aye against not Aye)

### Log loss

| Session | n | Model | B0 base rate | B1 party line | B2 majority-party sponsor | Best baseline | Model beats it | Skill |
|---|---|---|---|---|---|---|---|---|
| 2015–16 | 205761 | 0.2669 | 0.4358 | 1.5434 | 0.3555 | B2 majority-party sponsor | yes | 0.249 |
| 2017–18 | 222619 | 0.2778 | 0.4413 | 1.4204 | 0.3590 | B2 majority-party sponsor | yes | 0.226 |
| 2019–20 | 171667 | 0.2760 | 0.4106 | 1.3312 | 0.3381 | B2 majority-party sponsor | yes | 0.184 |
| 2021–22 | 221266 | 0.2946 | 0.4259 | 1.3369 | 0.3507 | B2 majority-party sponsor | yes | 0.160 |
| 2023–24 | 247522 | 0.2799 | 0.4036 | 1.3111 | 0.3308 | B2 majority-party sponsor | yes | 0.154 |
| **Pooled** | 1068835 | 0.2794 | 0.4234 | 1.3871 | 0.3467 | B2 majority-party sponsor | 5 of 5 | 0.194 (95% CI 0.189 to 0.199) |

Pooled 95% intervals (log loss): Model 0.2764 to 0.2823; B0 base rate 0.4196 to 0.4271; B1 party line 1.3682 to 1.4061; B2 majority-party sponsor 0.3439 to 0.3494.

### Brier score

| Session | n | Model | B0 base rate | B1 party line | B2 majority-party sponsor | Best baseline | Model beats it | Skill |
|---|---|---|---|---|---|---|---|---|
| 2015–16 | 205761 | 0.0732 | 0.1317 | 0.3337 | 0.1110 | B2 majority-party sponsor | yes | 0.340 |
| 2017–18 | 222619 | 0.0778 | 0.1346 | 0.3069 | 0.1107 | B2 majority-party sponsor | yes | 0.297 |
| 2019–20 | 171667 | 0.0770 | 0.1217 | 0.2875 | 0.1011 | B2 majority-party sponsor | yes | 0.239 |
| 2021–22 | 221266 | 0.0825 | 0.1284 | 0.2887 | 0.1061 | B2 majority-party sponsor | yes | 0.223 |
| 2023–24 | 247522 | 0.0775 | 0.1192 | 0.2831 | 0.0987 | B2 majority-party sponsor | yes | 0.214 |
| **Pooled** | 1068835 | 0.0777 | 0.1271 | 0.2997 | 0.1055 | B2 majority-party sponsor | 5 of 5 | 0.263 (95% CI 0.257 to 0.269) |

Pooled 95% intervals (Brier): Model 0.0766 to 0.0788; B0 base rate 0.1255 to 0.1287; B1 party line 0.2956 to 0.3038; B2 majority-party sponsor 0.1045 to 0.1064.

Noe (predicted when P(Aye) < 0.5), pooled: B0 base rate recall 0.000, precision —; B1 party line recall 0.935, precision 0.203; B2 majority-party sponsor recall 0.129, precision 0.295; Model recall 0.661, precision 0.703.

## Concurrence units (scored and reported separately; no pass rule)

### Passage, Brier

| Session | n | Model | B0 base rate | B1 party line | B2 majority-party sponsor | Best baseline | Model beats it | Skill |
|---|---|---|---|---|---|---|---|---|
| 2015–16 | 1569 | 0.0863 | 0.0782 | 0.2868 | 0.0765 | B2 majority-party sponsor | no | -0.127 |
| 2017–18 | 1712 | 0.0737 | 0.0713 | 0.2342 | 0.0710 | B2 majority-party sponsor | no | -0.037 |
| 2019–20 | 1173 | 0.0501 | 0.0457 | 0.2012 | 0.0467 | B0 base rate | no | -0.098 |
| 2021–22 | 1591 | 0.0449 | 0.0443 | 0.2024 | 0.0442 | B2 majority-party sponsor | no | -0.017 |
| 2023–24 | 1759 | 0.0732 | 0.0663 | 0.1933 | 0.0656 | B2 majority-party sponsor | no | -0.115 |
| **Pooled** | 7804 | 0.0667 | 0.0622 | 0.2241 | 0.0618 | B2 majority-party sponsor | 0 of 5 | -0.080 (95% CI -0.093 to -0.067) |

Pooled 95% intervals (Brier): Model 0.0617 to 0.0716; B0 base rate 0.0578 to 0.0665; B1 party line 0.2151 to 0.2335; B2 majority-party sponsor 0.0574 to 0.0661.

### Tally (not-Aye), MAE

| Session | n | Model | B0 base rate | B1 party line | B2 majority-party sponsor | Best baseline | Model beats it | Skill |
|---|---|---|---|---|---|---|---|---|
| 2015–16 | 1431 | 5.165 | 8.799 | 23.231 | 8.685 | B2 majority-party sponsor | yes | 0.405 |
| 2017–18 | 1577 | 4.648 | 7.956 | 21.034 | 7.663 | B2 majority-party sponsor | yes | 0.393 |
| 2019–20 | 1111 | 4.137 | 7.006 | 17.658 | 6.354 | B2 majority-party sponsor | yes | 0.349 |
| 2021–22 | 1520 | 3.883 | 6.525 | 17.268 | 6.156 | B2 majority-party sponsor | yes | 0.369 |
| 2023–24 | 1619 | 3.746 | 6.436 | 15.592 | 5.945 | B2 majority-party sponsor | yes | 0.370 |
| **Pooled** | 7258 | 4.310 | 7.338 | 18.948 | 6.965 | B2 majority-party sponsor | 5 of 5 | 0.381 (95% CI 0.370 to 0.392) |

Pooled 95% intervals (MAE): Model 4.213 to 4.413; B0 base rate 7.232 to 7.450; B1 party line 18.546 to 19.386; B2 majority-party sponsor 6.854 to 7.082.

### Member votes, log loss

| Session | n | Model | B0 base rate | B1 party line | B2 majority-party sponsor | Best baseline | Model beats it | Skill |
|---|---|---|---|---|---|---|---|---|
| 2015–16 | 96629 | 0.2139 | 0.3313 | 1.6911 | 0.2815 | B2 majority-party sponsor | yes | 0.240 |
| 2017–18 | 105626 | 0.2223 | 0.3426 | 1.5631 | 0.2795 | B2 majority-party sponsor | yes | 0.205 |
| 2019–20 | 74353 | 0.2321 | 0.3294 | 1.3655 | 0.2730 | B2 majority-party sponsor | yes | 0.150 |
| 2021–22 | 99087 | 0.2598 | 0.3734 | 1.4189 | 0.3078 | B2 majority-party sponsor | yes | 0.156 |
| 2023–24 | 108743 | 0.2361 | 0.3353 | 1.2793 | 0.2854 | B2 majority-party sponsor | yes | 0.173 |
| **Pooled** | 484438 | 0.2329 | 0.3430 | 1.4651 | 0.2860 | B2 majority-party sponsor | 5 of 5 | 0.186 (95% CI 0.178 to 0.194) |

Pooled 95% intervals (log loss): Model 0.2283 to 0.2379; B0 base rate 0.3371 to 0.3485; B1 party line 1.4398 to 1.4923; B2 majority-party sponsor 0.2813 to 0.2908.

## Counts

| Session | Units | With a roll call | Member votes | Bills | Fitted on | Training units |
|---|---|---|---|---|---|---|
| 2015–16 | 3862 | 3500 | 205761 | 2434 | 2009–10, 2011–12, 2013–14 | 11998 |
| 2017–18 | 4156 | 3777 | 222619 | 2619 | 2009–10, 2011–12, 2013–14, 2015–16 | 15860 |
| 2019–20 | 3181 | 2892 | 171667 | 2048 | 2009–10, 2011–12, 2013–14, 2015–16, 2017–18 | 20016 |
| 2021–22 | 4157 | 3737 | 221266 | 2545 | 2009–10, 2011–12, 2013–14, 2015–16, 2017–18, 2019–20 | 23197 |
| 2023–24 | 4505 | 4149 | 247522 | 2839 | 2009–10, 2011–12, 2013–14, 2015–16, 2017–18, 2019–20, 2021–22 | 27354 |

Units dropped and why, and each session's data: 2009–10: none dropped; 2011–12: {"passage: deciding vote has no member rows (tally and members not scored)": 4}; 2013–14: none dropped; 2015–16: none dropped; 2017–18: none dropped; 2019–20: {"concurrence: deciding vote has no member rows (tally and members not scored)": 2}; 2021–22: none dropped; 2023–24: none dropped.

The 2019–20 session (remote voting, a shortened calendar) is shown as it came out.
