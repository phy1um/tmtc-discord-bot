from constants import *
from discord.gateway_protocol import Gateway
from discord.api import DiscordAPI
import bot_config as config

from botaction import *

from action.assign_role import AssignRoleOnReact

import logging as log


log.basicConfig(encoding='utf-8', level=log.DEBUG)

class ReadyLogger(APIBotActor):
    def __init__(self, bot, cfg, gw, api):
        bot.define_event_handler(self.ready)

    async def ready(self, msg):
        log.info("gateway connection ready")



if __name__ == "__main__":
    import sys
    cfg = config.from_file("config.json")

    log_level = log.getLevelName(cfg.log_level)
    log.basicConfig(encoding='utf-8', level=log_level, stream=sys.stdout)
    logfile = open("log", "a")
    handler = log.StreamHandler(logfile)
    handler.setLevel(log.DEBUG)
    formatter = log.Formatter('[%(asctime)s][%(name)s:%(levelname)s]:: %(message)s')
    handler.setFormatter(formatter)
    log.getLogger().addHandler(handler)

    gw = Gateway(cfg.token)
    api = DiscordAPI(cfg.token)
    bot = APIBot(cfg, gw, api)

    bot.register_actor(ReadyLogger)
    bot.register_actor(AssignRoleOnReact, "emoji_roles")

    bot.run()

