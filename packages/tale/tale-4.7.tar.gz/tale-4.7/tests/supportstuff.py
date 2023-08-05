"""
Unittest support stuff

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""

import datetime
from typing import Any, List

from tale import pubsub, util, driver, base, story


class Thing:
    def __init__(self) -> None:
        self.x = []  # type: List[Any]

    def append(self, value: Any, ctx: util.Context) -> None:
        assert ctx.driver is not None and isinstance(ctx.driver, FakeDriver)
        self.x.append(value)


class FakeDriver(driver.Driver):
    def __init__(self) -> None:
        super().__init__()
        # fix up some essential attributes on the driver that are normally only present after loading a story file
        self.game_clock = util.GameDateTime(datetime.datetime.now())
        self.moneyfmt = util.MoneyFormatter.create_for(story.MoneyType.MODERN)
        assert len(self.commands.get([])) > 0


class Wiretap(pubsub.Listener):
    def __init__(self, target: base.Living) -> None:
        self.msgs = []  # type: List[Any]
        self.senders = []   # type: List[Any]
        tap = target.get_wiretap()
        tap.subscribe(self)

    def pubsub_event(self, topicname: pubsub.TopicNameType, event: Any) -> None:
        sender, message = event
        self.msgs.append((sender, message))
        self.senders.append(sender)

    def clear(self) -> None:
        self.msgs = []
        self.senders = []


class MsgTraceNPC(base.Living):
    def init(self) -> None:
        self._init_called = True
        self.messages = []  # type: List[str]

    def clearmessages(self) -> None:
        self.messages = []

    def tell(self, message: str, *, end: bool=False, format: bool=True) -> base.Living:
        self.messages.append(message)
        return self
