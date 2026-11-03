---
name: odds-check
description: >-
  Replays the rest of a trading day 10,000 times from the stock's own recent
  5-minute bars and reports how often a trade plan hits its target first, its
  stop first, or neither by the close, plus the average result in R. Use when
  the user asks "what are the odds", "run the time machine", "simulate this
  trade", "monte carlo", "backtest this setup", "is this a coin flip", or
  before the Breakout Bot takes a new paper trade.
argument-hint: "TICKER ENTRY STOP TARGET [HH:MM]"
---

# odds-check

A reality check before a paper trade, not a prediction.

## Steps

1. Get the plan: ticker, entry, stop, target and the entry time (exchange
   time, HH:MM). If any is missing, ask. Stop and target must sit on opposite
   sides of the entry.
2. Run:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/odds.py" --ticker TSLA --entry 364.18 --stop 358.32 --target 370.04 --at 10:15
   ```
   - If the Yahoo download fails (blocked network, rate limit), ask the user
     for a CSV of bars (`time,open,high,low,close`) and pass `--bars file.csv`.
   - Keep the default seed so the numbers can be reproduced; say which seed.
3. Report in plain words: target-first %, stop-first %, neither %, average R,
   how many sessions of history it used. Then one honest verdict, e.g. "close
   to a coin flip" or "the stop is hit more often than the target".
4. Append a line to `trader/journal.md` (create it if missing):
   `YYYY-MM-DD HH:MM | odds-check | TICKER | entry/stop/target | T% / S% / N% | avgR | verdict`

## Rules

- Always say it is a simulation from the last ~60 days and that earnings,
  halts and news can do things those days never did.
- Never call a result a guarantee or advice to buy.
- If a time slot has fewer than 20 past bars, say the odds are rough.
