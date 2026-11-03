# Claude setup: where each tip went

Built from 8 Instagram reels on Claude for trading (Nov 2026). Sources were
checked on GitHub and the web; claims that couldn't be confirmed are marked.

| Reel | Tip | What we did |
|---|---|---|
| eugene24752: Grok Bot + Robinhood | Strict rules, scheduled news checks, log everything, weekly grade vs holding, turn on trade approvals | Rules in `CLAUDE.md`; `/market-brief` and `/weekly-grade` skills; order-approval + order-log hook in `.claude/settings.json` |
| aimortal.ig: "test a trade 10,000×" | Time Machine from the open-source **day-trader-skill** pack (Jakeschincariol/day-trader-skill, MIT) | Our own `/odds-check` skill does the same bootstrap replay. The full 11-skill pack is an optional install (below) |
| msbintel: "One weekend, five builds" | TradingView MCP, CEO agent + sub-agents, daily brief, backtests, TimesFM 3 | Brief → `/market-brief`; backtest → `/odds-check`; TradingView MCP optional (below). TimesFM 3 skipped for now (heavy install, non-commercial weights) |
| msbintel: "Connecting Claude to TradingView" | tradesdontlie/tradingview-mcp | Optional, runs only on your own computer (below) |
| champmack: "Build 100 agents with 1 prompt" (`/ultracode`) | Big sub-agent teams | Built into Claude Code (`/effort` → ultracode in recent versions, per third-party guides). `CLAUDE.md` says to ask before big runs because they use a lot of usage |
| benkimball.ai: "5 MCPs you're missing" | #1 Perplexity (others not visible) | Skipped: Claude has web search built in; Perplexity MCP needs a paid API key |
| nateheherkai: "for investors" | Unknown (caption is only "comment WALLSTREET") | Not applied, waiting on a description |
| (8th reel) | Not received | — |

## Optional installs (on your own computer)

**11-skill day-trading pack.** Read the code first; it pulls free public data
(Yahoo, SEC, Nasdaq Trader, House Clerk) and can't place orders by itself.
Reviewed at commit `3d0f4ef`.

```bash
/plugin marketplace add Jakeschincariol/day-trader-skill
/plugin install day-trader-skill@day-trader-skill
```

**TradingView MCP** (unofficial). Needs TradingView Desktop with a paid plan,
Node 18+, and launching TradingView with `--remote-debugging-port=9222`. It
drives the desktop app through undocumented APIs, so it can break on updates.
Follow the README at github.com/tradesdontlie/tradingview-mcp, then register
it with `claude mcp add`.

## Scheduling the brief

In Claude Code on the web you can ask Claude to "schedule /market-brief
premarket at 8:45 AM ET on weekdays" and "/weekly-grade Fridays at 4:30 PM ET".
