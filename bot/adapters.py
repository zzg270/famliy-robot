from dataclasses import dataclass
from typing import Protocol


@dataclass
class GroupEvent:
    group_id: str
    sender_wxid: str
    sender_name: str
    content: str
    mentioned_wxid: str
    timestamp: int


class WeChatAdapter(Protocol):
    def send_text(self, group_id: str, content: str) -> None:
        ...

    def send_sticker(self, group_id: str, sticker_id: str) -> None:
        ...

    def send_voice(self, group_id: str, voice_file: str) -> None:
        ...

    def kick_member(self, group_id: str, member_wxid: str) -> None:
        ...


class MockWeChatAdapter:
    def send_text(self, group_id: str, content: str) -> None:
        print(f"[MOCK] TEXT -> group={group_id} content={content}")

    def send_sticker(self, group_id: str, sticker_id: str) -> None:
        print(f"[MOCK] STICKER -> group={group_id} sticker={sticker_id}")

    def send_voice(self, group_id: str, voice_file: str) -> None:
        print(f"[MOCK] VOICE -> group={group_id} file={voice_file}")

    def kick_member(self, group_id: str, member_wxid: str) -> None:
        print(f"[MOCK] KICK -> group={group_id} member={member_wxid}")
