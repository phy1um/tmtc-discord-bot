import logging as log
from discord.gateway import GatewayCon

LIB_NAME = "tmtc-dispy"


class Gateway(GatewayCon):

    def __init__(self, token):
        super().__init__(token)
        self._handlers = {}

    async def handle_message(self, msg):
        log.debug(f"gateway handle: {msg}")
        if msg.op == 10:
            log.info("recieve HELLO, sending identify")
            self._pulse = msg.data.heartbeat_interval / 1000
            identity = {
                "op": 2,
                "d": {
                    "token": self._token,
                    "intents": 1 << 10,
                    "properties": {
                        "$os": "linux",
                        "$browser": LIB_NAME,
                        "$device": LIB_NAME,
                    },
                }
            }
            await self.send(identity)
            log.info("done identify")
        elif msg.op == 0:
            event = msg.name.lower()
            if event in self._handlers:
                for h in self._handlers[event]:
                    await h(msg)
            else:
                log.debug(f"unhandled event {event}")
        else:
            raise Exception(f"unknown op in message {msg.op}")

    def event(self, f):
        fname = f.__name__
        if fname not in self._handlers:
            self._handlers[fname] = []
        self._handlers[fname].append(f)

if __name__ == "__main__":
    with open(".token") as token_file:
        token = token_file.read()[:-1]
        g = Gateway(token)

        @g.event
        async def ready(x):
            log.info("ready")

        @g.event
        async def message_reaction_add(x):
            log.info("reaction added")

        g.run()
        
