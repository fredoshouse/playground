#!/usr/bin/env python3
"""Tally The 30. Reads thirty/log/*.md, prints where you stand.

Usage:
    python3 score.py            # full standing
    python3 score.py --week 2   # one week
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

LOG_DIR = Path(__file__).parent / "log"
START = dt.date(2026, 9, 6)

POINTS = {
    "move": 3,
    "run": 2,
    "home": 2,
    "write": 3,
    "photo": 1,
    "pray": 2,
    "phone": 2,
    "sleep": 2,
}

# What a miss costs, in pushups.
PENALTY = {
    "move": 25,
    "home": 30,
    "write": 20,
    "phone": 15,
    "sleep": 15,
    "photo": 10,
    "pray": 20,
}
DAILY_DEBT_CAP = 100

UNLOCKS = [
    (90, "Full weekend — night out, one purchase, screens without guilt."),
    (75, "Pick ONE of the three. Deliberately."),
    (60, "Nothing discretionary. Rest, then earn it back."),
    (0, "No spend, no night out. This week's Big Rock goes to the top of next week."),
]

CHECK_RE = re.compile(r"^- \[(?P<mark>[ xX])\]\s*(?P<key>\w+)", re.M)
PAID_RE = re.compile(r"^paid:\s*(\d+)", re.M)
LINE_RE = re.compile(r"^## The line\n(.*?)(?=\n##|\Z)", re.M | re.S)


def today_pt():
    """The user's date, not UTC's — the check-ins run at 7am and 9:30pm Pacific."""
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=-7))).date()


class Day:
    def __init__(self, date, hits, paid, line):
        self.date = date
        self.hits = hits          # set of keys checked off
        self.paid = paid          # pushups already paid
        self.line = line

    @property
    def done(self):
        """A day still in progress owes nothing yet — you can't miss a day you're living."""
        return self.date < today_pt()

    @property
    def points(self):
        return sum(v for k, v in POINTS.items() if k in self.hits)

    @property
    def possible(self):
        # A non-run day tops out at 15; the run bonus only counts on run days.
        return sum(POINTS.values()) if "run" in self.hits else sum(POINTS.values()) - POINTS["run"]

    @property
    def owed(self):
        if not self.done:
            return 0
        raw = sum(v for k, v in PENALTY.items() if k not in self.hits)
        return min(raw, DAILY_DEBT_CAP)

    @property
    def grade(self):
        p = self.points
        return "A" if p >= 13 else "B" if p >= 11 else "C" if p >= 9 else "D"


def load():
    days = []
    for path in sorted(LOG_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        try:
            date = dt.date.fromisoformat(path.stem)
        except ValueError:
            print(f"skipping {path.name}: filename must be YYYY-MM-DD.md", file=sys.stderr)
            continue
        text = path.read_text()
        hits = {m["key"] for m in CHECK_RE.finditer(text) if m["mark"] in "xX"}
        paid = int(PAID_RE.search(text).group(1)) if PAID_RE.search(text) else 0
        line = LINE_RE.search(text)
        written = line.group(1).strip() if line else ""
        if written.startswith("("):      # untouched template placeholder
            written = ""
        days.append(Day(date, hits, paid, written))
    return days


def week_of(date):
    return (date - START).days // 7 + 1


def streak(days, key):
    """Current run of consecutive logged days ending at the most recent log."""
    n = 0
    for day in reversed(days):
        if key in day.hits:
            n += 1
        else:
            break
    return n


def unlock_for(total):
    return next(msg for floor, msg in UNLOCKS if total >= floor)


def report(days, only_week=None):
    if not days:
        print("No days logged yet. Copy log/_TEMPLATE.md to log/YYYY-MM-DD.md and start.")
        return

    weeks = {}
    for day in days:
        weeks.setdefault(week_of(day.date), []).append(day)

    for wk in sorted(weeks):
        if only_week and wk != only_week:
            continue
        wdays = weeks[wk]
        print(f"\n─── Week {wk} ─── {wdays[0].date} → {wdays[-1].date}")
        for d in wdays:
            if not d.done:
                print(f"  {d.date}  {d.points:>2}/{d.possible}  --  in progress")
                continue
            missed = [k for k in POINTS if k not in d.hits and k != "run"]
            tail = f"  missed: {', '.join(missed)}" if missed else "  clean"
            print(f"  {d.date}  {d.points:>2}/{d.possible}  {d.grade}{tail}")

        total = sum(d.points for d in wdays)
        owed = sum(d.owed for d in wdays)
        paid = sum(d.paid for d in wdays)
        print(f"\n  points   {total}/105")
        print(f"  workouts {sum('move' in d.hits for d in wdays)} (floor 4)"
              f"   runs {sum('run' in d.hits for d in wdays)} (floor 2)"
              f"   home {sum('home' in d.hits for d in wdays)} (floor 3)")
        print(f"  writing  {sum('write' in d.hits for d in wdays)} (floor 3)"
              f"   photos {sum('photo' in d.hits for d in wdays)}/7")
        print(f"  pushups  {owed} owed, {paid} paid, {max(owed - paid, 0)} outstanding")

        week_start = START + dt.timedelta(days=(wk - 1) * 7)
        left = max(7 - ((today_pt() - week_start).days + 1), 0)
        if left:
            # 15/day is the conservative ceiling — the run bonus isn't assumed.
            print(f"  unlock   holding at: {unlock_for(total)}")
            print(f"           {left} days left, still reachable: {unlock_for(total + 15 * left)}")
        else:
            print(f"  unlock   {unlock_for(total)}")

    if only_week:
        return

    print("\n═══ The 30 ═══")
    elapsed = (days[-1].date - START).days + 1
    print(f"  day {elapsed} of 30 — {len(days)} logged")
    print(f"  points        {sum(d.points for d in days)} / {sum(d.possible for d in days)}")
    print(f"  perfect days  {sum(d.points >= 15 for d in days)}")
    print(f"  home streak   {streak(days, 'home')}  (target 30)")
    print(f"  move streak   {streak(days, 'move')}")
    print(f"  write streak  {streak(days, 'write')}")
    outstanding = max(sum(d.owed for d in days) - sum(d.paid for d in days), 0)
    print(f"  pushup debt   {outstanding} outstanding")
    if outstanding:
        print(f"                pay it inside 48h or it doubles.")
    photos = sum('photo' in d.hits for d in days)
    print(f"  the story     {photos} photos, {sum(bool(d.line) for d in days)} lines written")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, help="report on a single week")
    args = ap.parse_args()
    report(load(), args.week)


if __name__ == "__main__":
    main()
