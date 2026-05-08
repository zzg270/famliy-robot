# Personal WeChat Group Bot MVP (Safe Simulation)

> ⚠️ This project is a **personal-playground simulation** for a dual-end bot architecture.
> It does **not** provide any reverse-engineering, protocol cracking, or account-risk bypass.

## What this MVP does

- Dual-end architecture:
  - **Control End**: manage welcome templates, target groups, and kick policies.
  - **Execution End**: consume "@ mention" events and execute responses.
- Auto welcome on mention:
  - text
  - sticker (simulated by sticker id)
  - voice (simulated by local voice file path)
- Auto kick policy with optional manual approval.
- Full local simulation via `MockWeChatAdapter`.

## Quick start

```bash
python3 app.py
```

You will see a simulated event stream. The bot will:
1. respond when mentioned in configured groups,
2. send text/sticker/voice welcome,
3. trigger kick flow on risk words.

## Why simulation first

For personal WeChat (non-WeCom), there is no stable official bot API for your full requirements.
This MVP helps you validate business flow first, then you can swap adapter implementation later.

## Files

- `app.py`: entry point with simulated events.
- `bot/core.py`: rule engine + orchestration.
- `bot/config.py`: runtime config models.
- `bot/adapters.py`: adapter interface and mock implementation.

