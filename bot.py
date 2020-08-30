import config

from discord.ext import commands
from aiohttp import ClientSession
from utils.context import AlphaCtx


class AlphaBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def config(self):
        return config

    async def get_context(self, message, *, cls=AlphaCtx):
        return await super().get_context(message, cls=cls)

    async def start(self, *args, **kwargs):
        self.session = ClientSession()
        await super().start(*args, **kwargs)

    async def close(self):
        await self.session.close()
        await super().close()


bot = AlphaBot(
    command_prefix=commands.when_mentioned_or("alpha ", "Alpha "),
    case_insensitive=True
)

bot.run(config.token)
