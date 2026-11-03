---
name: weekly-grade
description: >-
  Friday report card for the Breakout Bot: compares the bot's paper results for
  the week with simply buying and holding the same stock(s) and SPY, then
  grades the week and saves the report. Use when the user says "grade the
  bot", "weekly report", "how did the bot do", "did it beat holding", or on
  Fridays after the close.
argument-hint: "[week ending YYYY-MM-DD]"
---

# weekly-grade

## Steps

1. Pick the week: Monday to Friday ending on the given date (default: the most
   recent Friday). Use exchange time (New York).
2. Collect the bot's paper trades and decisions for that week from
   `trader/journal.md` and any bot trade log in `trader/`. If you can't find
   them, ask the user where the bot logs trades. Never guess trades.
3. Bot result: realized P&L in $ and %, number of trades, wins/losses, the
   largest loss, and how many "do nothing" decisions it made.
4. Benchmarks over the same window, same starting dollars:
   - buy-and-hold of the stock(s) the bot traded (equal-weight if several)
   - buy-and-hold of SPY
   Use Monday's open and Friday's close. Say where the prices came from.
5. Grade:
   - **A**: beat both benchmarks and stayed inside every limit
   - **B**: beat one benchmark, inside limits
   - **C**: beat neither, inside limits
   - **F**: broke any rule in CLAUDE.md, whatever the P&L
6. Save to `trader/grades/YYYY-MM-DD.md` with a small table (bot vs stock
   hold vs SPY), the grade, rule breaks, and one or two concrete things to
   change next week. Append a one-line summary to `trader/journal.md`.
7. Keep it honest: a single week is a tiny sample, so say so, and show the
   running record of past grades if earlier files exist.
