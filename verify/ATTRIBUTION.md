# Attribution for the files in `verify/inputs/`

These are byte-identical copies of the inputs the 11 November 2026 lock records cite, published so the locks can be reproduced. Each file's SHA-256 is in the `input_files` of every lock record in `predictions/2026-11-03/`.

## VoteHub · CC BY 4.0

- `data/votehub_raw/2026-10-07T024211/*.json`: the unmodified responses of VoteHub's `/polls` endpoint, one per race, fetched 2026-10-07. `MANIFEST.json` gives each file's URL, fetch time, size and SHA-256.
- `votehub_polls.json`: the processed snapshot the locks used.

Polling data via [VoteHub](https://votehub.com/polls/api/), licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). `votehub_polls.json` is a modified excerpt: PULSE INTEL filtered, deduplicated and reparsed it from the raw responses. It is not the original dataset.

## FiveThirtyEight · CC BY 4.0

- `data/538/pollster-ratings__pollster-ratings-combined.csv`: pollster ratings, including POLLSCORE.
- `data/538/pollster-ratings__2023__pollster-ratings.csv`: 2023 pollster ratings, including letter grades.

From FiveThirtyEight's data repository ([github.com/fivethirtyeight/data](https://github.com/fivethirtyeight/data), `pollster-ratings`), licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). The files are unmodified.

## FRED · Federal Reserve Bank of St. Louis

- `data/fred_snapshot.json`: economic series retrieved from FRED, Federal Reserve Bank of St. Louis ([fred.stlouisfed.org](https://fred.stlouisfed.org/)), on 2026-10-07.

It is collected, not used: the v61.40 forecasts do not run the fundamentals input. Each series belongs to its original source as credited on FRED.

## Cited but not redistributed

- `data/political_snapshots/2026-10-06/fiftyplusone-approval-president.html`
  - SHA-256 `b228ce8f2525d8fca1d707423b461b4eeb9d61bb6ec80aca6c3bf22fa0ce9bb6`
  - from https://fiftyplusone.news/polls/approval/president
- `data/political_snapshots/2026-10-06/fiftyplusone-generic-ballot.html`
  - SHA-256 `28d1d21d831ed4e6770ccb4c5af48f3ff500a8b8cb57fd70a9d57c85131b5024`
  - from https://fiftyplusone.news/polls/generic-ballot/generic-ballot

These are saved copies of FiftyPlusOne's web pages, fetched 2026-10-07. They are not republished here because they are a third party's site content. They are collected, not used, so no forecast number depends on them. Their URLs, fetch times, the figures read from them, and their hashes are in `data/political_snapshots/2026-10-06/MANIFEST.json`.

## Not public

The platform build (`pulse-intel-v6140.html`, SHA-256 `acca933752b328c06803ae6afd3615c731e134c6f949a328654bbb50ba5b7bb6`, pinned in every lock record) is not published. `reproduce_locks.py` recomputes the locks from the inputs above without it.
