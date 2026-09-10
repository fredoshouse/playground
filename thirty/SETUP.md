# What's wired up

All times Pacific. Day 1 = 2026-09-06, Day 30 = 2026-10-05.

## Email — alfred@fredoshouse.com
Two a day, sent by scheduled routines that resume this Claude session (which holds the
Gmail connection).

| When | Routine | What it does |
|------|---------|--------------|
| 9:30 PM | `The 30 — Nightly check-in` | Sweeps the last three days for replies you haven't been answered on, then sends where you stand, three questions, and what's still reachable. Sundays it adds the weekly review and unlock tier |
| 11:15 PM | `The 30 — Read replies` | Reads your reply, marks the day, commits it, and answers you in the same thread with your points, grade and streaks. Silent if you haven't replied |

**Replying works.** Hit reply on any check-in. "Yes, yes, 11" is a complete answer, so is a
paragraph. It gets read, scored, and acknowledged in the same thread — usually within a
couple of hours, and by the next night at the latest.

Say "stop" in a reply and the routines turn themselves off, with an email confirming it
and nothing lost.

The 7:00 AM morning routine is **disabled**. Two emails a day was too many for a system
nobody had started yet; it can be switched back on any time.

The evening routine also creates the day's log file (never overwriting one that already
has answers in it), and writes your answers into it when you reply — then commits and
pushes. You never have to touch a file.

Weeks run Sunday to Saturday. The Sunday review covers the week that just ended and sets
the one starting Monday; on Day 1 there's nothing behind it yet, so it's skipped.

It's UTC cron under the hood (`30 4 * * *`) but computes dates in `America/Los_Angeles`,
so log filenames are your dates, not UTC's.

## Calendar — alfred@fredoshouse.com

| Event | When |
|-------|------|
| Workout | Mon / Thu / Fri, 6:30 AM |
| Run — 3 miles | Tue / Sat, 6:30 AM |
| Write — 20 min / 500 words | Daily, 8:30 PM |
| Evening check-in | Daily, 9:30 PM |
| Phone out of the room | Daily, 10:15 PM |
| Sunday review + set the week | Sundays, 7:00 PM |
| Grocery run | Sundays, 11:00 AM |

Five workout slots for a floor of four — one is a built-in miss so a bad day doesn't
break the week.

All events end Oct 5.

## Turning it off
Ask, and the routines get deleted and the calendar series removed. Skipping a day is not
the same as quitting — say so in the check-in and the day gets adjusted instead of
counted as a miss.
