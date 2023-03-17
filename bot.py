from constants import *
from gateway_protocol import Gateway
from api import DiscordAPI
import bot_config as config

import logging as log


log.basicConfig(encoding='utf-8', level=log.DEBUG)


class Bot(object):
    def __init__(self, token):
        self.g = Gateway(token)
        self.api = DiscordAPI(token)

    def run_gateway(self):
        self.g.run()

    def event(self, f):
        return self.g.event(f)



if __name__ == "__main__":
    print("===  bot startup  ===")
    cfg = config.from_file("config.json")

    log_level = log.getLevelName(cfg.log_level)

    bot = Bot(cfg.token)

    @bot.event
    async def ready(x):
        log.info("gateway connection ready")

    @bot.event
    async def message_reaction_add(msg):
        emoji = msg.data.emoji["name"]
        if msg.data.message_id != cfg.message_id:
            # wrong message, do nothing
            log.debug(f"wrong message id, skipping")
            return

        if emoji not in cfg.emoji:
            # unknown emoji, do nothing
            log.debug(f"unknown emoji, skipping")
            return

        event_type = cfg.emoji[emoji]
        if event_type == "announcement":
            user_id = msg.data.user_id
            log.info(f"adding announce role to {user_id}") 
            bot.api.run(f"/guilds/{GUILD_ID}/members/{user_id}/roles/{ANNOUNCEMENT_ROLE}", "PUT")

    @bot.event
    async def message_reaction_remove(msg):
        emoji = msg.data.emoji["name"]
        if msg.data.message_id != cfg.message_id:
            log.debug(f"wrong message id, skipping remove")
            return
        if emoji not in cfg.emoji:
            log.debug(f"unknown emoji, skipping")
            return
        event_type = cfg.emoji[emoji]
        if event_type == "announcement":
            user_id = msg.data.user_id
            log.info("removing announce role from {user_id}")
            bot.api.run(f"/guilds/{GUILD_ID}/members/{user_id}/roles/{ANNOUNCEMENT_ROLE}", "DELETE")

    bot.run_gateway()

