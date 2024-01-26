from botaction import APIBotActor
import logging as log
import json
from types import SimpleNamespace

def _wrap(f, self):
    def wrapped(*args):
        return f(self, *args)
    return wrapped

class AssignRoleOnReact(APIBotActor):
    def __init__(self, bot, cfg, gw, api):
        super().__init__(bot, cfg, gw, api)   
        self._msgid = cfg.message_id
        self._emoji = cfg.emoji
        bot.define_event_handler(self.message_reaction_add)
        bot.define_event_handler(self.message_reaction_remove)
        self._roles = {}
        self._get_roles()

    def _get_roles(self):
        res = self.api.run(f"/guilds/{self._cfg.guild_id}/roles", "GET")
        for r in res:
            log.debug(f"found role {r['name']}")
            self._roles[r["name"]] = SimpleNamespace(**r) 

    async def message_reaction_add(self, msg):
        emoji = msg.data.emoji["name"]
        if msg.data.message_id != self._msgid:
            # wrong message, do nothing
            log.debug(f"wrong message id, skipping")
            return

        if emoji not in self._emoji:
            # unknown emoji, do nothing
            log.debug(f"unknown emoji, skipping")
            return

        event_type = self._emoji[emoji]
        if event_type not in self._roles:
            raise Exception(f"invalid role name: {event_type}")
        role = self._roles[event_type]
        user_id = msg.data.user_id
        log.info(f"adding role {role.name} to {user_id}") 
        self.bot.log(f"* Added role {role.name} to <@{user_id}>")
        self.api.run(f"/guilds/{self._cfg.guild_id}/members/{user_id}/roles/{role.id}", "PUT")

    async def message_reaction_remove(self, msg):
        emoji = msg.data.emoji["name"]
        if msg.data.message_id != self._msgid:
            log.debug(f"wrong message id, skipping remove")
            return
        if emoji not in self._emoji:
            log.debug(f"unknown emoji, skipping")
            return
        event_type = self._emoji[emoji]
        if event_type not in self._roles:
            raise Exception(f"invalid role name: {event_type}")
        role = self._roles[event_type]
        user_id = msg.data.user_id
        log.info(f"removing role {role.name} from {user_id}")
        self.bot.log(f"* Removing role {role.name} from <@{user_id}>")
        self.api.run(f"/guilds/{self._cfg.guild_id}/members/{user_id}/roles/{role.id}", "DELETE")

