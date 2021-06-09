import discord
import logging

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, config):
        self.config = config
        self.client = discord.Client()

        @self.client.event
        async def on_ready():
            logger.info("Discord client ready")

        @self.client.event
        async def on_message(message):
            # Don't respond to self
            if message.author == self.client.user:
                return

            prefix = self.config["bot"]["prefix"]
            if message.content == f"{prefix}ping":
                await message.channel.send("pong")

    async def run(self):
        try:
            await self.client.start(self.config["bot"]["token"])
        finally:
            if not self.client.is_closed():
                await self.client.close()
