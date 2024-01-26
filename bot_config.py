import logging as log
import json
import types

def from_file(fname):
    log.info(f"loading config from {fname}")
    with open(fname, encoding="utf-8") as json_file:
        o = json.load(json_file)
        token_file = o["token_file"]

        with open(token_file, encoding="utf-8") as f:
            token = f.read()[:-1]
            log.debug(f"read token: {token}")
            o["token"] = token
            return types.SimpleNamespace(**o)

