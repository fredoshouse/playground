# Letters

Where the writing lives, from a line said on a walk to something people can read.

```
letters/
├── topics.md     the running list — every idea, with status
├── seeds/        raw material with notes on what it still needs
├── drafts/       being written
└── published/    shipped, with where and when
```

## How a letter happens

1. **It gets said.** Usually in a check-in, usually about something else. The nightly
   routine pulls anything that sounds like a letter into `topics.md` as an idea.
2. **It gets said again.** That's the filter. A topic that comes back twice is real.
3. **Seed.** His words, cleaned up, plus honest notes on what's missing — the story, the
   turn, the landing.
4. **Draft.** Written in his voice (`thirty/voice/VOICE.md`), not summarized into it.
5. **Publish.** Beehiiv for the list, the site for the archive.

## Naming

`seeds/` and `drafts/` use a plain slug: `the-base.md`, `internal-comms.md`.

`published/` gets dated so the archive sorts itself: `2026-09-20-the-base.md`.

Each published file carries front matter, which is what any website or Beehiiv import
reads:

```yaml
---
title: The base
slug: the-base
date: 2026-09-20
status: published
channels: [beehiiv, site]
beehiiv_id: ""
summary: One line for the card and the preview text.
private: false
---
```

`private: true` means it never leaves this folder, whatever else is configured.

## Beehiiv, when you wire it up

Beehiiv has a v2 API — you'd add it as an MCP server and give it the publication ID and
an API key. Then a routine here can create a Beehiiv post from a draft, or pull stats
back after it sends. The important part is that **this folder stays the source of
truth** — Beehiiv is a distribution channel, not where the writing lives. If you ever
leave Beehiiv, the letters come with you.

The key goes in an environment variable. It never gets committed.
