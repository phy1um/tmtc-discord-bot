from botaction import APIBotActor

def AssignRoleOnReact(bot, cfg, gw, api):
    class _AssignRoleOnReact(APIBotActor):
        def __init__(self, bot, cfg, gw, api):
            super().__init__(cfg, bot, gw, api)   
            self._msgid = cfg.message_id
            self._emoji = cfg.emoji
            
        @bot.event
        async def message_reaction_add(msg):
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
            if event_type == "announcement":
                user_id = msg.data.user_id
                log.info(f"adding announce role to {user_id}") 
                self.api.run(f"/guilds/{GUILD_ID}/members/{user_id}/roles/{ANNOUNCEMENT_ROLE}", "PUT")

        @bot.event
        async def message_reaction_remove(msg):
            emoji = msg.data.emoji["name"]
            if msg.data.message_id != self._msgid:
                log.debug(f"wrong message id, skipping remove")
                return
            if emoji not in self._emoji:
                log.debug(f"unknown emoji, skipping")
                return
            event_type = self._emoji[emoji]
            if event_type == "announcement":
                user_id = msg.data.user_id
                log.info("removing announce role from {user_id}")
                self.api.run(f"/guilds/{GUILD_ID}/members/{user_id}/roles/{ANNOUNCEMENT_ROLE}", "DELETE")

    return _AssignRoleOnReact(bot, cfg, gw, api)
