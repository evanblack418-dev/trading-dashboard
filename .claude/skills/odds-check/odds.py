#!/usr/bin/env python3
"""Odds check: replay the rest of a trading day many times from the stock's own
recent intraday bars and count how often a plan hits its target first, its stop
first, or neither by the close.

Standard library only. It is a simulation built from recent history, not a
prediction.

Examples:
  python3 odds.py --ticker TSLA --entry 364.18 --stop 358.32 --target 370.04 --at 10:15
  python3 odds.py --bars bars.csv --entry 50 --stop 49 --target 52 --at 10:30 --sims 5000

--bars takes a CSV with columns: time,open,high,low,close
(time as ISO "YYYY-MM-DD HH:MM" in exchange-local time, regular session only).
Without --bars it downloads 60 days of 5-minute bars from Yahoo Finance's
public (unofficial) chart endpoint.
"""
import argparse
import csv
import datetime as dt
import json
import random
import sys
import urllib.request

UA = "Mozilla/5.0 (odds-check skill)"


def load_csv(path):
    days = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            t = dt.datetime.fromisoformat(row["time"].strip())
            bar = tuple(float(row[k]) for k in ("open", "high", "low", "close"))
            days.setdefault(t.date(), []).append((t.strftime("%H:%M"), bar))
    return days


def load_yahoo(ticker, interval, rng):
    url = ("https://query2.finance.yahoo.com/v8/finance/chart/%s?interval=%s&range=%s"
           "&includePrePost=false" % (ticker, interval, rng))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    res = data["chart"]["result"][0]
    off = res["meta"].get("gmtoffset", 0)
    q = res["indicators"]["quote"][0]
    days = {}
    for i, ts in enumerate(res.get("timestamp") or []):
        o, h, l, c = q["open"][i], q["high"][i], q["low"][i], q["close"][i]
        if None in (o, h, l, c):
            continue
        t = dt.datetime.utcfromtimestamp(ts + off)
        days.setdefault(t.date(), []).append((t.strftime("%H:%M"), (o, h, l, c)))
    return days


def slot_library(days, start):
    """For each time slot at or after `start`, collect each past bar as moves
    relative to the previous bar's close: (open, high, low, close) ratios."""
    lib = {}
    for bars in days.values():
        bars.sort()
        for (_, prev), (slot, bar) in zip(bars, bars[1:]):
            if slot < start:
                continue
            pc = prev[3]
            if pc <= 0:
                continue
            lib.setdefault(slot, []).append(tuple(x / pc for x in bar))
    return dict(sorted(lib.items()))


def simulate(lib, entry, stop, target, sims, seed):
    rnd = random.Random(seed)
    slots = list(lib)
    long_ = target > entry
    risk = abs(entry - stop)
    tally = {"target": 0, "stop": 0, "neither": 0}
    r_sum = 0.0
    for _ in range(sims):
        px = entry
        outcome = None
        for s in slots:
            o, h, l, c = rnd.choice(lib[s])
            hi, lo = px * h, px * l
            hit_stop = lo <= stop if long_ else hi >= stop
            hit_tgt = hi >= target if long_ else lo <= target
            if hit_stop:          # if both hit in one bar, assume the stop (conservative)
                outcome = "stop"
                break
            if hit_tgt:
                outcome = "target"
                break
            px *= c
        if outcome is None:
            outcome = "neither"
            r_sum += ((px - entry) if long_ else (entry - px)) / risk
        elif outcome == "target":
            r_sum += abs(target - entry) / risk
        else:
            r_sum -= 1.0
        tally[outcome] += 1
    return tally, r_sum / sims


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--ticker")
    src.add_argument("--bars", help="CSV of intraday bars")
    ap.add_argument("--entry", type=float, required=True)
    ap.add_argument("--stop", type=float, required=True)
    ap.add_argument("--target", type=float, required=True)
    ap.add_argument("--at", default="09:30", help="entry time HH:MM, exchange-local (default 09:30)")
    ap.add_argument("--interval", default="5m")
    ap.add_argument("--range", default="60d")
    ap.add_argument("--sims", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=19)
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    a = ap.parse_args()

    if (a.target > a.entry) == (a.stop > a.entry) or a.stop == a.entry:
        sys.exit("stop and target must be on opposite sides of the entry")

    days = load_csv(a.bars) if a.bars else load_yahoo(a.ticker, a.interval, a.range)
    lib = slot_library(days, a.at)
    if not lib:
        sys.exit("no bars at or after %s in the data" % a.at)
    depth = min(len(v) for v in lib.values())
    tally, avg_r = simulate(lib, a.entry, a.stop, a.target, a.sims, a.seed)
    pct = {k: round(100.0 * v / a.sims, 1) for k, v in tally.items()}
    out = {
        "source": a.bars or "Yahoo %s %s %s" % (a.ticker, a.interval, a.range),
        "sessions_in_data": len(days), "min_samples_per_slot": depth,
        "entry": a.entry, "stop": a.stop, "target": a.target, "from": a.at,
        "sims": a.sims, "seed": a.seed,
        "target_first_pct": pct["target"], "stop_first_pct": pct["stop"],
        "neither_by_close_pct": pct["neither"], "avg_R": round(avg_r, 3),
    }
    if a.json:
        print(json.dumps(out, indent=2))
        return
    print("Odds check: %s, %d sessions of history, %d replays (seed %d)"
          % (out["source"], len(days), a.sims, a.seed))
    print("  entry %.2f  stop %.2f  target %.2f  from %s" % (a.entry, a.stop, a.target, a.at))
    print("  target first      %5.1f %%" % pct["target"])
    print("  stop first        %5.1f %%" % pct["stop"])
    print("  neither by close  %5.1f %%" % pct["neither"])
    print("  average result    %+.2f R" % avg_r)
    if depth < 20:
        print("  warning: only %d past bars for some time slots; treat the odds as rough" % depth)
    print("Simulation from recent history, not a prediction. Not financial advice.")


if __name__ == "__main__":
    main()
