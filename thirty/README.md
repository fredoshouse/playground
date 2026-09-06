# The 30

An accountability system for Sept 6 → Oct 5, 2026. Seven scored dailies, a point total,
a pushup debt for misses, and a weekly unlock that puts the good stuff behind the work.

## The files

| File | What it's for |
|------|---------------|
| `CHARTER.md` | Why this exists, the seven dailies, September's Big Rocks. Read it when you don't feel like it. |
| `SCORING.md` | Points, penalties, unlocks, streaks. The rules of the game. |
| `CHECKIN.md` | The exact questions — morning, evening, Sunday. |
| `log/YYYY-MM-DD.md` | One file per day. Checkboxes + the day's one line. |
| `weekly/week-N.md` | Sunday review. |
| `score.py` | Does the math. |

## The daily loop

1. **Morning** — three framing questions from `CHECKIN.md`.
2. **Evening** — five questions. Answer in one line each; I fill the log.
3. `python3 thirty/score.py` — points, grade, streaks, what you owe.

## Starting a day

```bash
cp thirty/log/_TEMPLATE.md thirty/log/$(date +%F).md
```

Mark a win with `- [x]`. Record pushups you actually did on the `paid:` line.

## Checking the score

```bash
python3 thirty/score.py            # everything
python3 thirty/score.py --week 2   # one week
```

## The one rule that matters

Honest beats good. A logged D is worth more than an unlogged A — the whole thing only
works if the number is real.
