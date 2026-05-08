from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class WelcomeTemplate:
    text: str
    sticker_id: str
    voice_file: str


@dataclass
class KickPolicy:
    enabled: bool = False
    auto_kick: bool = False
    risk_words: List[str] = field(default_factory=lambda: ["广告", "拉人", "赌博"])


@dataclass
class BotConfig:
    bot_wxid: str
    enabled_groups: Set[str]
    welcome: WelcomeTemplate
    kick_policy: KickPolicy
    min_reply_interval_seconds: int = 30
