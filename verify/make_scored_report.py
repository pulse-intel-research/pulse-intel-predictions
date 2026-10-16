#!/usr/bin/env python3
"""
PULSE INTEL — the public scored-results report for the 11 November 2026 locks (v61.51)
======================================================================================
Reads the JSON that score_generals_2026.py --json writes and writes a Markdown report,
by default reports/2026-generals-scored.md. Every number in the report is a number in
that JSON, rounded for display; nothing is computed here except the rounding.

It refuses to run if:
  - any of the 11 lock records' SHA-256 differs from the hash pinned in the scorer
    (score_generals_2026.EXPECTED_LOCK_SHA256, imported from the scorer beside this file);
  - the JSON's locked figures differ from the lock records;
  - the JSON is a fixture run, unless --allow-fixtures (and then the report says so).

Run from the registry root, after the scorer:
  python3 verify/make_scored_report.py --scores scores.json --locks-dir predictions/2026-11-03
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_generals_2026 as scorer  # the pinned lock hashes live in the scorer, and only there

TOTAL_RACES = len(scorer.EXPECTED_LOCK_SHA256)
PENDING = ('no certified result file', 'result is not certified')


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pts(v):
    return ('+' if v > 0 else '−' if v < 0 else '') + '%.2f' % abs(v)


def pct(v, places=1):
    return ('%.' + str(places) + 'f%%') % v


def main():
    ap = argparse.ArgumentParser(description='Write the scored-results report from the scorer JSON.')
    ap.add_argument('--scores', required=True, help='the JSON written by score_generals_2026.py --json')
    ap.add_argument('--locks-dir', default='predictions/2026-11-03')
    ap.add_argument('--out', default='reports/2026-generals-scored.md')
    ap.add_argument('--allow-fixtures', action='store_true', help='report on a fixture run (test runs only)')
    args = ap.parse_args()

    locks_dir = Path(args.locks_dir)
    bad = []
    locks = {}
    for rid, want in sorted(scorer.EXPECTED_LOCK_SHA256.items()):
        p = locks_dir / (rid + '.json')
        if not p.exists() or sha256(p) != want:
            bad.append(rid)
        else:
            locks[rid] = json.loads(p.read_text())
    if bad:
        sys.exit('REFUSED: lock record hash does not match the pinned SHA-256 (or the record is missing): ' + ', '.join(bad))

    s = json.loads(Path(args.scores).read_text())
    if s.get('fixture_run') and not args.allow_fixtures:
        sys.exit('REFUSED: the scores are a fixture run, not certified results')
    hash_refusals = [x['race_id'] for x in s.get('refused', []) if 'hash' in x.get('reason', '') and 'lock record' in x.get('reason', '')]
    if hash_refusals:
        sys.exit('REFUSED: the scorer refused lock records on hash: ' + ', '.join(hash_refusals))
    races = {r['race_id']: r for r in s.get('races', [])}
    refused = {x['race_id']: x['reason'] for x in s.get('refused', [])}
    if set(races) | set(refused) != set(scorer.EXPECTED_LOCK_SHA256) or set(races) & set(refused):
        sys.exit('REFUSED: the scores do not cover each of the 11 locked races exactly once')
    for rid, r in races.items():
        P = locks[rid]['prediction']
        if (r['locked_margin'] != P['margin_c0_minus_c1_pts'] or r['predicted_winner'] != P['predicted_winner']
                or abs(r['win_probability'] * 100 - P['win_probability_predicted_winner_pct']) > 1e-9
                or r['interval_80'] != P['margin_interval_80'] or r['interval_95'] != P['margin_interval_95']):
            sys.exit('REFUSED: the scores for ' + rid + ' do not carry the lock record’s figures')

    t = s['totals']
    n = t['scored']
    partial = n < TOTAL_RACES
    tag = 'FIXTURE RUN — NOT RESULTS. ' if s.get('fixture_run') else ''
    L = []
    L.append('# November 2026 general elections: scored results')
    L.append('')
    if tag:
        L.append('**' + tag.strip() + '**')
        L.append('')
    L.append('Scored by `score_generals_2026.py` under `SCORING-2026-GENERALS.md` and its 2026-10-12 addendum. '
             'Races scored: %d of %d.%s' % (n, TOTAL_RACES, ' Partial: %d races are not yet scored.' % (TOTAL_RACES - n) if partial else ''))
    L.append('')
    L.append('Margins are the first-named candidate minus the second, in percentage points of all votes cast. '
             'Error is actual margin minus called margin.')
    L.append('')
    L.append('| Race | Candidates | Leader called | Win probability | Called margin | Actual margin | Error | Winner | Inside 80% range | Inside 95% range |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for rid in sorted(scorer.EXPECTED_LOCK_SHA256):
        P = locks[rid]['prediction']
        cands = P['candidate_c0'] + ' − ' + P['candidate_c1']
        if rid in races:
            r = races[rid]
            L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                rid, cands, r['predicted_winner'], pct(r['win_probability'] * 100), pts(r['locked_margin']),
                pts(r['actual_margin']), pts(r['error']), 'right' if r['winner_called'] else 'wrong',
                'yes' if r['inside_80'] else 'no', 'yes' if r['inside_95'] else 'no'))
        else:
            status = 'pending certification' if refused[rid] in PENDING else 'not scored: ' + refused[rid]
            # No number for a race the scorer did not score: every number in the report is the scorer's.
            L.append('| %s | %s | %s | — | — | — | — | %s | — | — |' % (rid, cands, P['predicted_winner'], status))
    L.append('')
    L.append('## Totals' + (' (partial: %d of %d races certified)' % (n, TOTAL_RACES) if partial else ''))
    L.append('')
    if n:
        lbl = ' (partial)' if partial else ''
        L.append('| Measure | Value |')
        L.append('|---|---|')
        L.append('| Winners right%s | %d of %d |' % (lbl, t['winners_called'], n))
        L.append('| Inside 80%% range%s | %d of %d (%s) |' % (lbl, t['inside_80'], n, pct(t['coverage_80_pct'])))
        L.append('| Inside 95%% range%s | %d of %d (%s) |' % (lbl, t['inside_95'], n, pct(t['coverage_95_pct'])))
        L.append('| Mean absolute error%s | %s points |' % (lbl, '%.2f' % t['mean_abs_error']))
        L.append('| Mean Brier score%s | %s |' % (lbl, '%.4f' % t['mean_brier']))
        L.append('')
        L.append('80%% range coverage%s: %s; published walk-forward backtest (METHODOLOGY-v61.40 addendum, 2026-10-08): %s.' % (
            lbl, pct(t['coverage_80_pct']), pct(t['addendum_walkforward_t1_pct']['80'])))
    else:
        L.append('No race is certified yet; there are no totals.')
    L.append('')
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(L))
    print('wrote ' + str(out) + ' · %d of %d races scored%s' % (n, TOTAL_RACES, ' (partial)' if partial else ''))


if __name__ == '__main__':
    main()
