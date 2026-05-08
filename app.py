from bot.adapters import GroupEvent, MockWeChatAdapter
from bot.config import BotConfig, KickPolicy, WelcomeTemplate
from bot.core import BotEngine


def build_engine() -> BotEngine:
    config = BotConfig(
        bot_wxid="wxid_bot",
        enabled_groups={"group_tech", "group_game"},
        welcome=WelcomeTemplate(
            text="欢迎 {user}，已收到你的@，祝你聊得开心！",
            sticker_id="sticker_smile_01",
            voice_file="assets/welcome_voice.mp3",
        ),
        kick_policy=KickPolicy(
            enabled=True,
            auto_kick=False,
            risk_words=["广告", "博彩", "引流"],
        ),
        min_reply_interval_seconds=10,
    )
    return BotEngine(config=config, adapter=MockWeChatAdapter())


def main() -> None:
    engine = build_engine()

    events = [
        GroupEvent("group_tech", "wxid_alice", "Alice", "@wxid_bot 新人报道", "wxid_bot", 100),
        GroupEvent("group_tech", "wxid_spam", "SpamGuy", "@wxid_bot 来看博彩广告", "wxid_bot", 120),
        GroupEvent("group_other", "wxid_bob", "Bob", "@wxid_bot hello", "wxid_bot", 140),
    ]

    for event in events:
        print(f"\n[EVENT] {event}")
        engine.handle_event(event)

    print("\n[CONTROL END] manual approve queued kicks...")
    while engine.approve_next_kick():
        pass


if __name__ == "__main__":
    main()
