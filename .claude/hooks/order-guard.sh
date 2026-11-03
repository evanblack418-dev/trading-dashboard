#!/usr/bin/env bash
# PreToolUse / PostToolUse hook for broker order tools (Alpaca, Robinhood, IBKR, ...).
# Pre:  forces a permission prompt for every order, even if the tool was set to "Always allow".
# Post: appends the order request to trader/order-log.jsonl so every decision is logged.
set -euo pipefail
input="$(cat)"
event="$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("hook_event_name",""))')"
root="${CLAUDE_PROJECT_DIR:-.}"

if [ "$event" = "PostToolUse" ]; then
  mkdir -p "$root/trader"
  printf '%s' "$input" | python3 -c '
import json, sys, datetime
d = json.load(sys.stdin)
print(json.dumps({"logged_at": datetime.datetime.now().isoformat(timespec="seconds"),
                  "tool": d.get("tool_name"), "input": d.get("tool_input")}))' >> "$root/trader/order-log.jsonl"
  exit 0
fi

cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Order tool: paper money only (see CLAUDE.md). Confirm this exact order, account type (paper) and limit price before allowing."}}
JSON
