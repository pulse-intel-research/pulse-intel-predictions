#!/usr/bin/env python3
"""
Reproduce the 11 November 2026 general-election locks from their inputs alone.

Standalone: Python 3 standard library only, no platform build. It implements the
v61.40 method as METHODOLOGY-v61.40.md and its 2026-10-08 addendum state it,
from the input files in verify/inputs/ (byte-identical copies of the files the
lock records cite, each checked against the SHA-256 in the record; the build and two
saved third-party pages are not redistributed, see NOT_REDISTRIBUTED), and compares
the result with each lock record in predictions/2026-11-03/.

Run from the registry root:   python3 verify/reproduce_locks.py
Prints MATCH or MISMATCH per race; exits non-zero on any mismatch or input problem.

The method, as documented (METHODOLOGY-v61.40.md, "The method"):
  - Input: the VoteHub snapshot (votehub_polls.json, vintage 2026-10-07T02:42:11Z).
    Partisan-sponsored and internal polls are excluded; one row is kept per fielding
    (pollster, start date, end date), LV preferred; a poll must give a number for
    both principal candidates.
  - Weight of each poll = 0.5 ^ (age_days / 30) x its 538 weight, age measured from
    the poll's end date to the forecast as-of date (2026-10-07). A poll ending after
    the as-of date is left out.
  - 538 weight = clip(1 - (POLLSCORE + 1) / 3, 0.1, 1), rounded to 0.01, from the
    archived 538 ratings, matching the pollster's name after lower-casing and removing
    everything but letters and digits; unrated pollsters get 1.0. The methodology names
    a letter-grade fallback when POLLSCORE is absent but does not state its table: if a
    used poll would need it, this script stops and says so rather than guess.
  - Margin = weighted average share of c0 minus that of c1.
  - sigma = max(poll sigma, 4.67), poll sigma = max(1.8, 0.7 x recency-weighted mean MoE),
    MoE = 98 / sqrt(n). The floor binds in every locked race.
  - Win probability of c0 = Phi(margin / sigma), Phi by Abramowitz-Stegun 26.2.17, no clamp.
  - Ranges: margin +/- 1.282 x sigma (80%) and +/- 1.96 x sigma (95%).

Stored precision (as in the records): margins and ranges to 0.01, win probability to 0.1,
rounded half away from zero on the exact binary value (JavaScript toFixed).

What it does not do: re-derive votehub_polls.json from the raw VoteHub responses (that
parser is in the private platform repository). The raw responses are included and checked
against their manifest's hashes, and votehub_polls.json against the lock records' hash.
"""

import csv
import glob
import hashlib
import json
import math
import os
import re
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.dirname(HERE)
INPUTS = os.path.join(HERE, 'inputs')
LOCKS = os.path.join(REGISTRY, 'predictions', '2026-11-03')
SIGMA_FLOOR = 4.67          # METHODOLOGY-v61.40.md: the historical polling-average error
HALF_LIFE_DAYS = 30
Z80, Z95 = 1.282, 1.96
# Cited by every lock record but not redistributed here: full saved copies of a third party's web
# pages (FiftyPlusOne). They are "collected, not used" — no forecast number depends on them — and
# their SHA-256, URL and fetch time are in verify/inputs/data/political_snapshots/2026-10-06/MANIFEST.json
# and verify/ATTRIBUTION.md. Only these exact paths are excused from the presence check.
NOT_REDISTRIBUTED = {
    'data/political_snapshots/2026-10-06/fiftyplusone-approval-president.html',
    'data/political_snapshots/2026-10-06/fiftyplusone-generic-ballot.html',
}


def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def fixed(x, places):
    """JavaScript Number.prototype.toFixed: nearest, halves away from zero, on the exact binary value."""
    q = Decimal(1).scaleb(-places)
    return float(Decimal(x).quantize(q, rounding=ROUND_HALF_UP))


def phi(x):
    """Standard normal CDF, Abramowitz & Stegun 26.2.17."""
    b1, b2, b3, b4, b5, p = 0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429, 0.2316419
    t = 1.0 / (1.0 + p * abs(x))
    pdf = math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)
    upper = pdf * t * (b1 + t * (b2 + t * (b3 + t * (b4 + t * b5))))
    return 1.0 - upper if x >= 0 else upper


def norm_name(s):
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower())


def load_538():
    combined, graded = {}, set()
    with open(os.path.join(INPUTS, 'data', '538', 'pollster-ratings__pollster-ratings-combined.csv'), newline='') as f:
        for r in csv.DictReader(f):
            if r['POLLSCORE'] not in ('', None):
                w = 1 - (float(r['POLLSCORE']) + 1) / 3
                combined[norm_name(r['pollster'])] = fixed(min(1.0, max(0.1, w)), 2)
    with open(os.path.join(INPUTS, 'data', '538', 'pollster-ratings__2023__pollster-ratings.csv'), newline='') as f:
        for r in csv.DictReader(f):
            if r['538 Grade']:
                graded.add(norm_name(r['Pollster']))
    return combined, graded


def weight_538(pollster, combined, graded):
    n = norm_name(pollster)
    if n in combined:
        return combined[n]
    if n in graded:
        raise SystemExit('STOP: ' + pollster + ' needs the letter-grade fallback, whose table METHODOLOGY-v61.40.md does not state')
    return 1.0


def ingest(raw, c0, c1):
    """The documented exclusions, in order: partisan/internal; one row per fielding (LV preferred); both shares present."""
    rank = {'lv': 0, 'rv': 1, 'a': 2, 'v': 3}
    groups = {}
    for p in raw:
        if p.get('partisan') is not None or p.get('internal') is True:
            continue
        groups.setdefault((p['pollster'], p.get('startDate'), p['date']), []).append(p)
    kept = [sorted(rows, key=lambda p: rank.get(p.get('population'), 9))[0] for rows in groups.values()]
    return [p for p in kept if isinstance(p.get(c0), (int, float)) and isinstance(p.get(c1), (int, float))]


def recompute(polls, c0, c1, as_of, combined, graded):
    asof = date.fromisoformat(as_of)
    used = [p for p in polls if date.fromisoformat(p['date']) <= asof]
    # Canonical order (newest first, then source id), so the sum is order-independent.
    used.sort(key=lambda p: (-date.fromisoformat(p['date']).toordinal(), str(p.get('sourceId', ''))))
    s0 = s1 = sw = moe = moe_w = 0.0
    for p in used:
        rw = 0.5 ** ((asof - date.fromisoformat(p['date'])).days / HALF_LIFE_DAYS)
        w = rw * weight_538(p['pollster'], combined, graded)
        s0 += p[c0] * w
        s1 += p[c1] * w
        sw += w
        if p.get('sample'):
            moe += (98 / math.sqrt(p['sample'])) * rw
            moe_w += rw
    a0, a1 = s0 / sw, s1 / sw
    margin = fixed(a0 - a1, 2)
    poll_sigma = max(1.8, 0.7 * (moe / moe_w if moe_w else 3.5))
    sigma = max(poll_sigma, SIGMA_FLOOR)
    win_c0 = fixed(phi(margin / sigma) * 100, 1)
    return {
        'n': len(used), 'margin': margin, 'sigma': sigma,
        'leader': c0 if margin >= 0 else c1,
        'win_c0': win_c0,
        'win_leader': win_c0 if margin >= 0 else fixed(100 - win_c0, 1),
        'pi80': {'low': fixed(margin - Z80 * sigma, 2), 'high': fixed(margin + Z80 * sigma, 2)},
        'pi95': {'low': fixed(margin - Z95 * sigma, 2), 'high': fixed(margin + Z95 * sigma, 2)},
    }


def main():
    records = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(LOCKS, '*.json')))]
    if len(records) != 11:
        raise SystemExit('expected 11 lock records, found %d' % len(records))

    # Every input a record cites (except the build, which is not public) must be here, byte for byte.
    problems = []
    for rec in records:
        for f in rec['input_files']:
            if f['role'] == 'build' or f['path'] in NOT_REDISTRIBUTED:
                continue
            path = os.path.join(INPUTS, f['path'])
            if not os.path.exists(path):
                problems.append(rec['race_id'] + ': missing ' + f['path'])
            elif sha256(path) != f['sha256']:
                problems.append(rec['race_id'] + ': ' + f['path'] + ' does not match its SHA-256')
    manifest = json.load(open(os.path.join(INPUTS, 'data', 'votehub_raw', '2026-10-07T024211', 'MANIFEST.json')))
    for rid, f in manifest['files'].items():
        if sha256(os.path.join(INPUTS, 'data', 'votehub_raw', '2026-10-07T024211', f['file'])) != f['sha256']:
            problems.append('raw VoteHub response ' + f['file'] + ' does not match its manifest')
    if problems:
        print('\n'.join('INPUT PROBLEM: ' + p for p in sorted(set(problems))))
        sys.exit(2)
    cited = {f['path']: f['sha256'] for rec in records for f in rec['input_files']}
    snap = json.load(open(os.path.join(INPUTS, 'data', 'political_snapshots', '2026-10-06', 'MANIFEST.json')))['files']
    for path in sorted(NOT_REDISTRIBUTED):
        if snap[os.path.basename(path)]['sha256'] != cited[path]:
            print('INPUT PROBLEM: the manifest\'s hash for ' + path + ' differs from the lock records\'')
            sys.exit(2)
    published = sum(1 for p in cited if p != 'pulse-intel-v6140.html' and p not in NOT_REDISTRIBUTED)
    print('inputs: %d of the %d files the records cite are here and match their SHA-256; raw responses match their manifest' % (published, len(cited)))
    print('        not here: the build (not public) and %d saved third-party pages (not used; hashes in the manifest)' % len(NOT_REDISTRIBUTED))

    snapshot = json.load(open(os.path.join(INPUTS, 'votehub_polls.json')))
    combined, graded = load_538()
    mismatches = 0
    for rec in records:
        P = rec['prediction']
        c0, c1 = re.sub(r' \([DR]\)$', '', P['candidate_c0']), re.sub(r' \([DR]\)$', '', P['candidate_c1'])
        polls = ingest(snapshot['races'].get(rec['race_id'], []), c0, c1)
        r = recompute(polls, c0, c1, rec['forecast_as_of'], combined, graded)
        checks = [
            ('leader', P['predicted_winner'], r['leader']),
            ('margin', P['margin_c0_minus_c1_pts'], r['margin']),
            ('win probability', P['win_probability_predicted_winner_pct'], r['win_leader']),
            ('80% range', P['margin_interval_80'], r['pi80']),
            ('95% range', P['margin_interval_95'], r['pi95']),
        ]
        bad = [(k, a, b) for k, a, b in checks if a != b]
        if bad:
            mismatches += 1
            print('MISMATCH %-11s %s' % (rec['race_id'], '; '.join('%s: record %s, recomputed %s' % x for x in bad)))
        else:
            print('MATCH    %-11s %s, margin %+.2f, %.1f%%, 80%% [%.2f, %.2f], 95%% [%.2f, %.2f], %d polls' % (
                rec['race_id'], r['leader'], r['margin'], r['win_leader'], r['pi80']['low'], r['pi80']['high'],
                r['pi95']['low'], r['pi95']['high'], r['n']))
    print('%d of %d locks reproduce' % (len(records) - mismatches, len(records)))
    sys.exit(1 if mismatches else 0)


if __name__ == '__main__':
    main()
