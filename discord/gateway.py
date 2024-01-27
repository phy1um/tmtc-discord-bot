import asyncio
import websockets
import json
import traceback

from dataclasses import dataclass
from types import SimpleNamespace

import logging as log

GATEWAY_URL = "wss://gateway.discord.gg/"

@dataclass
class GatewayMessage():
    op: int
    data: object
    sequence: int
    name: str

def decode_msg(msg):
    obj = json.loads(msg) 
    data = None
    seq = None
    name = None
    if "d" in obj and obj["d"] is not None:
        data = SimpleNamespace(**obj["d"])
    if "s" in obj:
        seq = obj["s"]
    if "t" in obj:
        name = obj["t"]
    return GatewayMessage(obj["op"], data, seq, name)

class GatewayCon(object):
    def __init__(self, token):
        log.info("init Gateway Connection")
        self._token = token
        self._q = asyncio.Queue()
        self._pulse = 0.9
        self._run = True

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run_connection())

    async def _run_connection(self):
        log.info("running Gateway")
        wsurl = f"{GATEWAY_URL}/?v=9&encoding=json"
        send = asyncio.create_task(self._send_loop())
        ping = asyncio.create_task(self._ping_loop())
        async for ws in websockets.connect(wsurl, close_timeout=1):
            self._ws = ws
            recv = asyncio.create_task(self._recv_loop())
            await recv


    async def _recv_loop(self):
        async for msg in self._ws:
            if msg == None:
                continue
            decoded = decode_msg(msg)
            log.debug(f"decoded = {decoded}")
            try:
                await self.handle_message(decoded)
            except Exception as e:
                log.error(f"exception in handler: {e}")
                traceback.print_exc()
        log.debug("recv loop: websocket closed")

    async def _send_loop(self):
        while self._run:
            try:
                msg = await self._q.get()
                strmsg = json.dumps(msg)
                log.debug(f"gateway send: {msg}")
                self._q.task_done()
                await self._ws.send(strmsg)
            except Exception as e:
                log.error(f"exception in send: {e}")
                traceback.print_exc()
                await ws.close()

    async def _ping_loop(self):
        while self._run:
            try:
                await asyncio.sleep(self._pulse)
                log.debug("sending DISCORD ping")
                ping = {"op": 1, "d": None}
                await self.send(ping)
            except Exception as e:
                log.error(f"exception in ping: {e}")
                traceback.print_exc()

    async def handle_message(self, msg):
        pass

    async def send(self, msg):
        log.debug("pushing msg to send")
        await self._q.put(msg)

class GatewayPrinter(GatewayCon):
    async def handle_message(self, msg):
        print(msg)


if __name__ == "__main__":
    con = GatewayPrinter("foo")
    con.run()

