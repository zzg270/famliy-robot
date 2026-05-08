from dataclasses import dataclass, field
from typing import Dict, List

from bot.adapters import GroupEvent, WeChatAdapter
from bot.config import BotConfig


@dataclass
class PendingKick:
    group_id: str
    member_wxid: str
    reason: str


@dataclass
class BotEngine:
    config: BotConfig
    adapter: WeChatAdapter
    last_reply_ts: Dict[str, int] = field(default_factory=dict)
    pending_kicks: List[PendingKick] = field(default_factory=list)

    def handle_event(self, event: GroupEvent) -> None:
        if event.group_id not in self.config.enabled_groups:
            return
        if event.mentioned_wxid != self.config.bot_wxid:
            return

        if not self._rate_limit_ok(event):
            print(f"[INFO] Skip due to rate limit: group={event.group_id}")
            return

        self._welcome(event)
        self._moderate(event)

    def approve_next_kick(self) -> bool:
        if not self.pending_kicks:
            return False
        kick = self.pending_kicks.pop(0)
        self.adapter.kick_member(kick.group_id, kick.member_wxid)
        print(f"[INFO] Approved kick for {kick.member_wxid}, reason={kick.reason}")
        return True

    def _rate_limit_ok(self, event: GroupEvent) -> bool:
        last_ts = self.last_reply_ts.get(event.group_id, -10**9)
        if event.timestamp - last_ts < self.config.min_reply_interval_seconds:
            return False
        self.last_reply_ts[event.group_id] = event.timestamp
        return True

    def _welcome(self, event: GroupEvent) -> None:
        text = self.config.welcome.text.format(user=event.sender_name)
        self.adapter.send_text(event.group_id, text)
        self.adapter.send_sticker(event.group_id, self.config.welcome.sticker_id)
        self.adapter.send_voice(event.group_id, self.config.welcome.voice_file)

    def _moderate(self, event: GroupEvent) -> None:
        policy = self.config.kick_policy
        if not policy.enabled:
            return

        lowered = event.content.lower()
        hit_word = next((w for w in policy.risk_words if w.lower() in lowered), None)
        if not hit_word:
            return

        reason = f"hit risk word: {hit_word}"
        if policy.auto_kick:
            self.adapter.kick_member(event.group_id, event.sender_wxid)
            print(f"[INFO] Auto kicked {event.sender_wxid}, reason={reason}")
            return

        self.pending_kicks.append(
            PendingKick(event.group_id, event.sender_wxid, reason)
        )
        print(f"[INFO] Pending kick queued for {event.sender_wxid}, reason={reason}")
