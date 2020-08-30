"""
Alphabet Discord Bot

This bot helps manage all necessary administration and
automation for the Alphabet Discord server.

Author(s):
Pyro      - https://github.com/Pyroseza
Agent     - https://github.com/solidassassin
"""


from aiohttp import ClientSession
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


    async def get_context(self, message, *, cls=AlphaCtx):
        return await super().get_context(message, cls=cls)


    async def start(self, *args, **kwargs):
        self.session = ClientSession()
        token = self.config.get("token")
        # await super().start(*args, **kwargs)
        await super().start(token)


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
