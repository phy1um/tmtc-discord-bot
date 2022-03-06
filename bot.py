from constants import *
from gateway_protocol import Gateway
from api import DiscordAPI

WELCOME_MSG_ID = "943445168235900939"

class Bot(object):
    def __init__(self, token):
        self.g = Gateway(token)
        self.api = DiscordAPI(token)

    def run_gateway(self):
        self.g.run()

    def event(self, f):
        return self.g.event(f)

if __name__ == "__main__":
    token = "foo"
    with open(".token") as token_file:
        token = token_file.read()[:-1]

    bot = Bot(token)

    @bot.event
    async def message_reaction_add(msg):
        emoji = msg.data.emoji["name"]
        if msg.data.message_id != WELCOME_MSG_ID:
            return
        if emoji == "🔴":
            print("adding announce role") 
            user_id = msg.data.user_id
            bot.api.run(f"/guilds/{GUILD_ID}/members/{user_id}/roles/{ANNOUNCEMENT_ROLE}", "PUT")
        else:
            return

    bot.run_gateway()
