#!/usr/bin/env python3
"""
PULSE INTEL — score the 11 November 2026 general-election locks (v61.47)
========================================================================
Implements pulse-intel-predictions/SCORING-2026-GENERALS.md, which was committed
to the registry before any result existed. The rules live there; this script
follows them and nothing else.

Inputs
  - The 11 v61.40 lock records in pulse-intel-predictions/predictions/2026-11-03/.
    Each file's SHA-256 must equal the value pinned below (and in the rules);
    otherwise that race is refused.
  - One certified result per race: data/results_2026/<race_id>.json (format in
    SCORING-2026-GENERALS.md and data/results_2026/README.md), with the certified
    source document saved beside it and its SHA-256 recorded. A race with no
    certified result, or whose source document does not match its hash, is refused.

Output
  A table on stdout and, with --json PATH, the same numbers as JSON. It writes
  nothing else: no lock record, no result, no registry file.

Fixtures
  A results file with "fixture": true is refused unless --allow-fixtures is given,
  and then every line of output says FIXTURE RUN — NOT RESULTS.

Run:  python3 score_generals_2026.py [--json scores.json]
"""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
LOCKS = REPO / 'pulse-intel-predictions' / 'predictions' / '2026-11-03'
RESULTS = REPO / 'data' / 'results_2026'

# SHA-256 of each lock record as committed to the registry (commit 6d37251), and as
# pinned in the v61.40 build. Pinned again in SCORING-2026-GENERALS.md.
EXPECTED_LOCK_SHA256 = {
    'fl-gov-gen': 'f9ea45ccd56f750d211255a7e8e0de9c6c9c11cea0535896f3eb86277ae05b40',
    'ga-gov-gen': '6442cba22035f6bff497dc65ccb941a0e830906c06344b1e0048902a647cac4e',
    'ga-sen-gen': '95eaedc42168f263740e6302b20fdc1ede26c85e2f53dd534295ae555b60a995',
    'ia-gov-gen': 'ced89a266c0d7ec7292f7a2cac67c3da545de346d129c7c03f62f4917f3b635b',
    'ia-sen-gen': '4864f3171106f3e50bcc09d04bfe56c0f26d1d7974ff8dcf65cefb019647c019',
    'me-sen-gen': 'c7658cd4ec271aa43aa67dcc5b3dd53396eadcc9fbfe75f7f9463ffd466722a1',
    'mi-sen-gen': '0303196e9c088f52244418e50e7aab88478b616a00e2c61eafe74641666447d6',
    'nc-sen-gen': '4e1c019509b3853247939fc3f0e4bc473303d7689786b0971a7f6f99cbc23869',
    'nh-sen-gen': '85666d16b7562fc78bf190e4053e0eb63f0e3984990607bc110d607ac881eaa4',
    'oh-sen-gen': '6c8b4409fb50df3a7dfc0032d0c39b9a13529da2b51f856d07ca4ac86b206eca',
    'tx-sen-gen': '56288682172161efe642ac053e8a6c1df15e48102bbb985e2d2ea2e8bd2d8821',
}
# Maine Senate's lock used only two-way polls (head-to-head or ranked-choice final
# round), so it is scored on the ranked-choice final round. Every other race is
# scored on the November 3 general-election count.
ROUND = {rid: 'general' for rid in EXPECTED_LOCK_SHA256}
ROUND['me-sen-gen'] = 'rcv-final'
REQUIRED = ['race_id', 'certified', 'certified_date', 'round', 'd_candidate', 'r_candidate', 'd_votes', 'r_votes',
            'total_votes', 'source_url', 'retrieved', 'source_file', 'sha256']
# The walk-forward coverage the addendum (METHODOLOGY-v61.40-addendum-2026-10-08.md) found at T−1.
ADDENDUM_COVERAGE = {'80': 70.8, '95': 88.9}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def name_and_party(label):
    """'Abdul El-Sayed (D)' -> ('Abdul El-Sayed', 'D')."""
    name, _, party = label.rpartition(' (')
    return name, party.rstrip(')')


def load_result(race_id, results_dir, allow_fixtures):
    """Returns (result, None) or (None, reason refused)."""
    path = results_dir / (race_id + '.json')
    if not path.exists():
        return None, 'no certified result file'
    try:
        r = json.loads(path.read_text())
    except ValueError:
        return None, 'result file is not valid JSON'
    missing = [k for k in REQUIRED if k not in r]
    if missing:
        return None, 'result file is missing ' + ', '.join(missing)
    if r.get('fixture') is True and not allow_fixtures:
        return None, 'result file is a fixture, not a certified result'
    if r['race_id'] != race_id:
        return None, 'result file names race ' + str(r['race_id'])
    if r['certified'] is not True:
        return None, 'result is not certified'
    if r['round'] != ROUND[race_id]:
        return None, 'result round is ' + str(r['round']) + '; this race is scored on ' + ROUND[race_id]
    for k in ('d_votes', 'r_votes', 'total_votes'):
        if not isinstance(r[k], int) or isinstance(r[k], bool) or r[k] < 0:
            return None, k + ' is not a non-negative whole number'
    if r['d_votes'] + r['r_votes'] > r['total_votes'] or r['total_votes'] == 0:
        return None, 'total_votes is smaller than the two candidates’ votes'
    src = (results_dir / r['source_file']).resolve()
    if results_dir.resolve() not in src.parents:
        return None, 'source_file is outside the results directory'
    if not src.exists():
        return None, 'certified source document is not saved at ' + r['source_file']
    if sha256(src) != r['sha256']:
        return None, 'certified source document does not match its sha256'
    return r, None


def score_race(lock, result):
    p = lock['prediction']
    n0, party0 = name_and_party(p['candidate_c0'])
    n1, party1 = name_and_party(p['candidate_c1'])
    if {party0, party1} != {'D', 'R'}:
        return None, 'lock record is not one D and one R'
    if result['d_candidate'] != (n0 if party0 == 'D' else n1) or result['r_candidate'] != (n0 if party0 == 'R' else n1):
        return None, 'result candidates do not match the lock record'
    v0 = result['d_votes'] if party0 == 'D' else result['r_votes']
    v1 = result['r_votes'] if party0 == 'D' else result['d_votes']
    actual = 100.0 * (v0 - v1) / result['total_votes']          # c0 − c1, points of all votes cast
    locked = p['margin_c0_minus_c1_pts']
    winner_is_c0 = p['predicted_winner'] == n0
    if actual == 0:
        called = False                                           # an exact tie is not a correct call
        outcome = 0.5
    else:
        called = (actual > 0) == winner_is_c0
        outcome = 1.0 if called else 0.0
    prob = p['win_probability_predicted_winner_pct'] / 100.0
    i80, i95 = p['margin_interval_80'], p['margin_interval_95']
    return {
        'race_id': lock['race_id'], 'candidate_c0': p['candidate_c0'], 'candidate_c1': p['candidate_c1'],
        'predicted_winner': p['predicted_winner'], 'actual_leader': (n0 if actual > 0 else n1 if actual < 0 else 'tie'),
        'winner_called': called,
        'locked_margin': locked, 'actual_margin': actual, 'error': actual - locked, 'abs_error': abs(actual - locked),
        'inside_80': i80['low'] <= actual <= i80['high'], 'inside_95': i95['low'] <= actual <= i95['high'],
        'interval_80': i80, 'interval_95': i95,
        'win_probability': prob, 'brier': (prob - outcome) ** 2,
        'result': {k: result[k] for k in ('round', 'd_votes', 'r_votes', 'total_votes', 'source_url', 'retrieved', 'certified_date', 'sha256')},
    }, None


def main():
    ap = argparse.ArgumentParser(description='Score the 11 November 2026 general-election locks.')
    ap.add_argument('--results-dir', default=str(RESULTS))
    ap.add_argument('--locks-dir', default=str(LOCKS))
    ap.add_argument('--allow-fixtures', action='store_true', help='score fixture files (test runs only)')
    ap.add_argument('--json', help='also write the scores as JSON to this path')
    args = ap.parse_args()
    results_dir, locks_dir = Path(args.results_dir), Path(args.locks_dir)

    races, refused = [], []
    for race_id in sorted(EXPECTED_LOCK_SHA256):
        lock_path = locks_dir / (race_id + '.json')
        if not lock_path.exists():
            refused.append({'race_id': race_id, 'reason': 'lock record missing'})
            continue
        if sha256(lock_path) != EXPECTED_LOCK_SHA256[race_id]:
            refused.append({'race_id': race_id, 'reason': 'lock record hash does not match the pinned sha256'})
            continue
        lock = json.loads(lock_path.read_text())
        result, why = load_result(race_id, results_dir, args.allow_fixtures)
        if why:
            refused.append({'race_id': race_id, 'reason': why})
            continue
        row, why = score_race(lock, result)
        if why:
            refused.append({'race_id': race_id, 'reason': why})
            continue
        row['fixture'] = result.get('fixture') is True
        races.append(row)

    n = len(races)
    totals = {'scored': n, 'refused': len(refused)}
    if n:
        totals.update({
            'winners_called': sum(r['winner_called'] for r in races),
            'mean_abs_error': sum(r['abs_error'] for r in races) / n,
            'mean_signed_error': sum(r['error'] for r in races) / n,
            'inside_80': sum(r['inside_80'] for r in races), 'coverage_80_pct': 100.0 * sum(r['inside_80'] for r in races) / n,
            'inside_95': sum(r['inside_95'] for r in races), 'coverage_95_pct': 100.0 * sum(r['inside_95'] for r in races) / n,
            'expected_coverage_pct': {'80': 80.0, '95': 95.0}, 'addendum_walkforward_t1_pct': ADDENDUM_COVERAGE,
            'mean_brier': sum(r['brier'] for r in races) / n,
        })
    fixture_run = any(r['fixture'] for r in races)
    out = {'rules': 'pulse-intel-predictions/SCORING-2026-GENERALS.md', 'fixture_run': fixture_run, 'races': races, 'refused': refused, 'totals': totals}

    tag = 'FIXTURE RUN — NOT RESULTS · ' if fixture_run else ''
    f2 = lambda v: ('+' if v > 0 else '−' if v < 0 else '') + '%.2f' % abs(v)
    print(tag + 'Scoring the November 2026 general-election locks (rules: SCORING-2026-GENERALS.md)')
    for r in races:
        print(tag + '%-11s called %-5s  locked %7s  actual %7s  error %7s  80%% %-3s  95%% %-3s  Brier %.4f' % (
            r['race_id'], 'right' if r['winner_called'] else 'WRONG', f2(r['locked_margin']), f2(r['actual_margin']), f2(r['error']),
            'in' if r['inside_80'] else 'OUT', 'in' if r['inside_95'] else 'OUT', r['brier']))
    for x in refused:
        print(tag + '%-11s NOT SCORED — %s' % (x['race_id'], x['reason']))
    if n:
        t = totals
        print(tag + 'Totals over %d scored: winners called %d/%d · mean absolute error %.2f · mean signed error %s · '
              'inside 80%% %d/%d (%.1f%%; nominal 80%%, addendum walk-forward %.1f%%) · inside 95%% %d/%d (%.1f%%; nominal 95%%, addendum %.1f%%) · mean Brier %.4f' % (
                  n, t['winners_called'], n, t['mean_abs_error'], f2(t['mean_signed_error']), t['inside_80'], n, t['coverage_80_pct'], ADDENDUM_COVERAGE['80'],
                  t['inside_95'], n, t['coverage_95_pct'], ADDENDUM_COVERAGE['95'], t['mean_brier']))
    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
