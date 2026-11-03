---
name: market-brief
description: >-
  Writes a short pre-market or midday market brief for the Breakout Bot's
  watchlist: overnight and pre-market moves, headlines that could move each
  stock, earnings or events today, and what that means for the bot's rules.
  Saves it to trader/briefs/. Use when the user says "market brief", "morning
  brief", "what's moving", "check the news before the open", or on a schedule
  before 9:30 AM ET and around midday.
argument-hint: "[premarket|midday] [TICKER ...]"
---

# market-brief

## Steps

1. Watchlist: tickers given in the arguments, else `trader/watchlist.txt`
   (one ticker per line), else ask the user.
2. For each ticker, use web search (and any market-data tool you have) to get:
   - last close and current/pre-market price and % change, with source + time
   - top 1-3 headlines from the last 24h, each with source and timestamp
   - scheduled events today: earnings, guidance, FDA, splits, index changes
3. Market backdrop: SPY and QQQ pre-market move, any big macro release today
   (CPI, jobs, Fed) with its time.
4. Flag rule conflicts from CLAUDE.md, e.g. "TSLA reports after the close, so
   a day trade must be flat before then".
5. Save to `trader/briefs/YYYY-MM-DD-<premarket|midday>.md`, under one screen
   long, in this order: backdrop, per-ticker table, flags, sources.
6. Append a one-line entry to `trader/journal.md`.

## Rules

- Facts with sources only. No buy/sell calls, no price targets. Not advice.
- If a source can't be reached, say so instead of filling the gap.
- Headlines older than 24h go under "older", not in the main table.
