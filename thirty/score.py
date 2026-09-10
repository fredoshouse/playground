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

# Days 1-3 ran the seven-daily version, went unlogged, and are void. The design was
# too big to start with; that's not a debt he owes. Scoring restarts here.
RESET = dt.date(2026, 9, 9)

# Three dailies. Body, money, sleep. The other four come back once there's a streak
# worth protecting — see CHARTER.md.
POINTS = {
    "move": 3,
    "home": 2,
    "sleep": 2,
}

# What a miss costs, in pushups.
PENALTY = {
    "move": 25,
    "home": 30,
    "sleep": 15,
}
DAILY_DEBT_CAP = 100
# Debt that can't be paid stops being a consequence and becomes a reason to quit.
TOTAL_DEBT_CAP = 300

DAY_MAX = sum(POINTS.values())      # 7
WEEK_MAX = DAY_MAX * 7              # 49

# Shares of what was actually scoreable that week, not of a flat 49 — a week with void
# days still has a reachable top tier.
UNLOCKS = [
    (0.90, "Full weekend — night out, one purchase, screens without guilt."),
    (0.75, "Pick ONE of the three. Deliberately."),
    (0.60, "Nothing discretionary. Rest, then earn it back."),
    (0.0, "No spend, no night out. This week's Big Rock goes to the top of next week."),
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
    def untouched(self):
        """Never logged at all — different from a logged day that went badly."""
        return not self.hits and not self.paid and not self.line

    @property
    def void(self):
        """Ran under the abandoned seven-daily design. Not scored, not charged."""
        return self.date < RESET

    @property
    def done(self):
        """A day still in progress owes nothing yet — you can't miss a day you're living."""
        return self.date < today_pt()

    @property
    def points(self):
        if self.void:
            return 0
        return sum(v for k, v in POINTS.items() if k in self.hits)

    @property
    def possible(self):
        return 0 if self.void else DAY_MAX

    @property
    def owed(self):
        if not self.done or self.void:
            return 0
        raw = sum(v for k, v in PENALTY.items() if k not in self.hits)
        return min(raw, DAILY_DEBT_CAP)

    @property
    def grade(self):
        p = self.points
        return "A" if p >= DAY_MAX else "B" if p >= 5 else "C" if p >= 3 else "D"


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


def stalled(days):
    """Consecutive unlogged days at the end — the system talking to itself."""
    n = 0
    for day in reversed(days):
        if day.done and day.untouched:
            n += 1
        else:
            break
    return n


def unlock_for(total, ceiling):
    share = total / ceiling if ceiling else 0
    return next(msg for floor, msg in UNLOCKS if share >= floor)


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
        live = [d for d in wdays if not d.void]
        print(f"\n─── Week {wk} ─── {wdays[0].date} → {wdays[-1].date}")
        for d in wdays:
            if d.void:
                print(f"  {d.date}   --      void (pre-reset)")
            elif not d.done:
                print(f"  {d.date}  {d.points:>2}/{DAY_MAX}   in progress")
            elif d.untouched:
                window = "backfillable" if (today_pt() - d.date).days <= 2 else "locked"
                print(f"  {d.date}   0/{DAY_MAX}   not logged ({window})")
            else:
                missed = [k for k in POINTS if k not in d.hits]
                tail = f"  missed: {', '.join(missed)}" if missed else "  clean"
                print(f"  {d.date}  {d.points:>2}/{DAY_MAX}   {d.grade}{tail}")

        if not live:
            continue
        # Scoreable days in this week's Sun-Sat window: void days can't be earned back.
        week_start = START + dt.timedelta(days=(wk - 1) * 7)
        scoreable = sum(1 for i in range(7) if (week_start + dt.timedelta(days=i)) >= RESET)
        ceiling = scoreable * DAY_MAX
        total = sum(d.points for d in live)
        owed = sum(d.owed for d in live)
        paid = sum(d.paid for d in live)
        print(f"\n  points   {total}/{ceiling}" + (f"  ({scoreable} scoreable days)" if ceiling != WEEK_MAX else ""))
        print(f"  moved {sum('move' in d.hits for d in live)} (floor 4)"
              f"   ate home {sum('home' in d.hits for d in live)} (floor 3)"
              f"   in bed on time {sum('sleep' in d.hits for d in live)}")
        print(f"  pushups  {owed} owed, {paid} paid, {max(owed - paid, 0)} outstanding")

        # Days still winnable in this week, today included — today isn't over yet.
        floor_day = max(today_pt(), RESET)
        remaining = sum(1 for i in range(7) if (week_start + dt.timedelta(days=i)) >= floor_day)
        if remaining:
            banked = sum(d.points for d in live if d.done)
            print(f"  unlock   holding at: {unlock_for(total, ceiling)}")
            print(f"           {remaining} days still winnable, best case: "
                  f"{unlock_for(banked + DAY_MAX * remaining, ceiling)}")
        else:
            print(f"  unlock   {unlock_for(total, ceiling)}")

    if only_week:
        return

    live = [d for d in days if not d.void]
    print("\n═══ The 30 ═══")
    print(f"  day {(days[-1].date - START).days + 1} of 30 — {len(live)} scored since the reset")
    print(f"  points        {sum(d.points for d in live)} / {sum(d.possible for d in live)}")
    print(f"  clean days    {sum(d.points == DAY_MAX for d in live)}")
    print(f"  home streak   {streak(days, 'home')}  (target 30)")
    print(f"  move streak   {streak(days, 'move')}")
    print(f"  sleep streak  {streak(days, 'sleep')}")
    raw_debt = max(sum(d.owed for d in live) - sum(d.paid for d in live), 0)
    outstanding = min(raw_debt, TOTAL_DEBT_CAP)
    print(f"  pushup debt   {outstanding} outstanding{' (capped)' if raw_debt > TOTAL_DEBT_CAP else ''}")
    if outstanding:
        print("                pay it inside 48h or it doubles.")

    stall = stalled([d for d in live])
    if stall >= 2:
        print(f"\n  !! {stall} days unlogged in a row since the reset.")
        print("     Three dailies and one email was already the smaller version.")
        print("     Ask him directly whether to stop.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, help="report on a single week")
    args = ap.parse_args()
    report(load(), args.week)


if __name__ == "__main__":
    main()
