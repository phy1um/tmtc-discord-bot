import websockets
import json
import sys
import asyncio
import gateway
import random

hello_msg = {
        "t": None,
        "s": None,
        "op": 10,
        "d": {
            "heartbeat_interval": 2000,
            "_trace": ["[\"gateway-prd-main-zmlr\",{\"micros\":0.0}]"]
        }
    }

ready_msg = {
        "t": "READY",
        "s": 1,
        "op": 0,
        "d": {
            "v": 9,
            "user_settings": {},
            "user": { "username": "fake_user", "id": "12345", "bot": True },
            "session_id": "abcdefg",
            "relationships": [],
            "private_channels": [],
            "precenses": [],
            "guilds": [],
        }
    }

reaction_add_msg = {
  "t": "MESSAGE_REACTION_ADD",
  "s": 2,
  "op": 0,
  "d": {
    "user_id": "12345",
    "message_id": "12345",
    "member": {
      "user": {
        "username": "fake_user",
        "id": "12345",
        "discriminator": "9999",
        "avatar": "9999999999"
      },
      "roles": [],
      "nick": "Tom Marks",
      "mute": False,
      "joined_at": "2021-08-22T09:00:24.543000+00:00",
      "hoisted_role": "12345",
      "deaf": False
    },
    "emoji": {
      "name": "😠",
      "id":None 
    },
    "channel_id": "11111111111111",
    "guild_id": "222222222222222"
  }
}



async def server_fn(ws):
    print(f"new connection @ {ws}")
    hello_str = json.dumps(hello_msg)
    await ws.send(hello_str)
    async for msg in ws:
        o = gateway.decode_msg(msg)
        if o.op == 11:
            # send random event after pings
            if random.random() > 0.8:
                await ws.send(json.dumps(reaction_add_msg))
        elif o.op == 2:
            # this is identify
            await ws.send(json.dumps(ready_msg))
        else:
            print("BAD MESSAGE")



async def serve(host, port):
    async with websockets.serve(server_fn, host, port):
        await asyncio.Future()


if __name__ == "__main__":
    print(f"running ws server @ ws://localhost:{sys.argv[1]}")
    asyncio.run(serve("localhost", sys.argv[1]))
