import logging as log
import json

class ConfigFieldMissingException(Exception):
    def __init__(self, n):
        super().__init__(self)
        self._field = n

    def __str__(self):
        return f"Could not find required field in config \"{self._field}\""

class Config(object):
    def __init__(self, token, emoji, msg_id, log):
        self._fname = ""
        self.token = token
        self.emoji = emoji
        self.message_id = msg_id
        self.log_level = log

def _get_field(o, n):
    if n not in o:
        raise ConfigFieldMissingException(n)
    return o[n]
    
def from_file(fname):
    log.info(f"loading config from {fname}")
    with open(fname, encoding="utf-8") as json_file:
        o = json.load(json_file)
        token_file = _get_field(o, "token_file")
        msg = _get_field(o, "message_id")
        emoji_map = _get_field(o, "emoji_roles")
        emoji = {}

        for k, v in emoji_map.items():
            log.debug(f"mapping emoji: {v} -> {k}")
            emoji[v] = k

        log_level = _get_field(o, "log_level")

        with open(token_file, encoding="utf-8") as f:
            token = f.read()[:-1]
            log.debug(f"read token: {token}")
            return Config(token, emoji, msg, log_level)

