# The 30

Three things a day, every day, through Oct 5, 2026. Move. Eat at home. In bed by 10:30.

One email a night at 9:30. Hit reply — "yes, yes, 11" is a complete answer. It gets read,
scored, and answered in the same thread.

## Where everything lives

```
thirty/
├── system/      the rules
│   ├── CHARTER.md    why this exists, the three dailies, September's Big Rocks
│   ├── SCORING.md    points, pushup debt, backfill window, unlock tiers
│   └── CHECKIN.md    the questions — nightly and Sunday
├── voice/
│   └── VOICE.md      who's writing the emails, and how
├── ops/
│   ├── SETUP.md      what's wired up: routines, calendar, delivery
│   └── score.py      does the math
├── log/         one file per day
└── weekly/      Sunday reviews
```

## Checking the score

```bash
python3 thirty/ops/score.py            # everything
python3 thirty/ops/score.py --week 2   # one week
```

## Starting a day by hand

Normally the nightly routine does this for you.

```bash
cp thirty/log/_TEMPLATE.md thirty/log/$(date +%F).md
```

Mark a win with `- [x]`. Pushups you actually did go on the `paid:` line.

## The rule that matters

Honest beats good. A logged D is worth more than an unlogged A — the whole thing only
works if the number is real.
