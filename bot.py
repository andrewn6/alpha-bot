<<<<<<< HEAD
"""
Alphabet Discord Bot

This bot helps manage all necessary administration and
automation for the Alphabet Discord server.

Author(s):
Pyro      - https://github.com/Pyroseza
Agent     - https://github.com/solidassassin
"""


from aiohttp import ClientSession
from discord.ext import commands
from pathlib import Path
from utils.config import Config
from utils.context import AlphaCtx
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(name)s -> %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


class AlphaBot(commands.Bot):
    """
    The main bot class where are the magic happens
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config().load()


    async def on_ready(self):
        log.info(f"{self.user} is in!")


    async def get_context(self, message, *, cls=AlphaCtx):
        return await super().get_context(message, cls=cls)

    @property
    def module_list(self):
        m = list(Path("cogs").glob("*.py"))
        all_cogs = [f"cogs.{i.name}"[:-3] for i in m]
        return all_cogs


    async def load_modules(self):
        _output = []
        for cog in self.module_list:
            try:
                self.load_extension(cog)
                _output.append(f"[{cog}] loaded")
            except commands.ExtensionAlreadyLoaded:
                _output.append(f"[{cog}] already loaded")
            except commands.ExtensionNotLoaded:
                _output.append(f"[{cog}] not loaded")
                log.exception(f"Failed to load {cog}")
        return "\n".join(_output)


    async def start(self, *args, **kwargs):
        self.session = ClientSession()
        await self.load_modules()
        token = self.config.get("token")
        if not token:
            raise KeyError("Token not found in config!")
        # await super().start(*args, **kwargs)
        await super().start(token, *args, **kwargs)


    async def close(self):
        await self.session.close()
        await super().close()


# create the alphabot instance
bot = AlphaBot(
    command_prefix=commands.when_mentioned_or("alpha ", "Alpha "),
    case_insensitive=True
)


@bot.event
async def on_ready():
    main_id = bot.config.get('main_guild')
    bot.main_guild = bot.get_guild(main_id) or bot.guilds[0]
    print('\nActive in these guilds/servers:')
    [print(g.name) for g in bot.guilds]
    print('\nMain guild:', bot.main_guild.name)
    print('\nAlphabot started successfully')
    return True


bot.run()
print('Alphabot has terminated')
