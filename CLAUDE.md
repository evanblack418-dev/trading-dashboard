# Breakout Bot Tracker

A password-locked page for a **paper-money** trading experiment (school project).

## How this repo works

- `index.html` is **generated and encrypted** by the trading bot (commits named
  "live refresh" / "dashboard update" by `trading-bot`). Never hand-edit it,
  never try to decrypt it, and never put the page password in any file,
  commit, or chat log. Change the generator, not the output.
- Bot working files (journal, plans, briefs, grades) live in `trader/`.

## Trading rules (standing, apply to every session)

1. **Paper money only.** Never connect a live brokerage account, never place a
   real-money order, and never store broker keys in the repo. If asked to,
   stop and confirm with the user first.
2. **Every order needs an explicit yes** from the user for that exact order,
   even on paper. Limit orders only. No margin, options, short selling or
   leverage unless the user turns them on in writing.
3. **Hard limits** come from `trader/config.json` (max $ per trade, max loss per
   trade, max trades per day). If the file is missing, ask; don't invent limits.
4. **Log every decision** (trade, skip, or "do nothing") in `trader/journal.md`:
   `YYYY-MM-DD HH:MM | skill/action | TICKER | what | why | data source + time`.
5. **Grade against just holding.** Every Friday, run `/weekly-grade`: compare
   the bot to buy-and-hold of the same stock(s) and SPY over the same week.
6. **Honesty about odds.** Backtests and simulations (`/odds-check`) are
   reality checks, not predictions. Always state sample size and time window.
   Never say "guaranteed", and nothing here is financial advice.

## Working style

- Market data: say where every number came from and when it was fetched.
  Yahoo's chart endpoint is unofficial; double-check anything important.
- Big, parallel jobs (research across many tickers, a full refactor) may use
  sub-agents, but ask before launching a large team or an `ultracode` run,
  because those burn through usage quickly.
- Before installing any third-party skill, plugin or MCP server, read its code,
  pin it to a commit, and tell the user what it can reach.

## Skills in this repo

| Command | Use |
|---|---|
| `/odds-check` | Replay the rest of the day 10,000× from recent 5-min bars: target-first / stop-first / neither odds |
| `/market-brief` | Pre-market or midday brief on the watchlist, saved to `trader/briefs/` |
| `/weekly-grade` | Friday report card: bot vs buy-and-hold vs SPY |

See `docs/claude-setup.md` for where each tip came from and optional add-ons.
