# What's wired up

All times Pacific. Day 1 = 2026-09-06, Day 30 = 2026-10-05.

## Email — alfred@fredoshouse.com
Two a day, sent by scheduled routines that resume this Claude session (which holds the
Gmail connection).

| When | Routine | What it sends |
|------|---------|---------------|
| 7:00 AM | `The 30 — Morning framing` | Today's scheduled work, the "one thing" you named last night quoted back, three framing questions, outstanding pushup debt |
| 9:30 PM | `The 30 — Evening check-in` | Where you stand, the five questions, what tonight costs if it's a zero. On Sundays it sends the weekly review and unlock tier instead |

The evening routine also creates the day's log file, and writes your answers into it when
you reply — then commits and pushes. You never have to touch a file.

Both are UTC cron under the hood (`0 14 * * *` and `30 4 * * *`) but compute dates in
`America/Los_Angeles`, so log filenames are your dates, not UTC's.

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
