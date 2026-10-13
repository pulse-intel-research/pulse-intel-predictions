# Scoring rules · November 2026 general elections · addendum, 2026-10-12

Addendum to [`SCORING-2026-GENERALS.md`](SCORING-2026-GENERALS.md), which is not edited.

**One change: where the results are published.** [`SCORING-2026-GENERALS.md`](SCORING-2026-GENERALS.md) places the certified result files at `data/results_2026/<race_id>.json` and their source documents under `data/results_2026/sources/`, both in the platform repository. Instead they will be published in this registry:

- each race's certified result file at `results_2026/<race_id>.json`;
- its certified source document under `results_2026/sources/`.

This change was made on 2026-10-12, before any result existed.

Nothing else changes. Every scoring rule, every definition, the result-file format and fields, the refusal conditions, the totals, and every pinned hash stay exactly as in [`SCORING-2026-GENERALS.md`](SCORING-2026-GENERALS.md). The pinned hashes are the SHA-256 of each of the 11 lock records and of `score_generals_2026.py`.
