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

class AlphaBot(commands.Bot):
    """
    The main bot class where are the magic happens
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config().load()
        self.log = kwargs.get("logger")


    async def on_ready(self):
        self.log.info(f"{self.user} is in!")


    async def get_context(self, message, *, cls=AlphaCtx):
        return await super().get_context(message, cls=cls)

    def user_is_ignored(self, user):
        user_roles = [role.id for role in user.roles]
        if self.config.get('ignore_role') in user_roles:
            return True
        return False


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
                self.log.exception(f"Failed to load {cog}")
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


def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s: %(name)s -> %(message)s",
        datefmt="%H:%M:%S",
    )
    log = logging.getLogger(__name__)

    # create the alphabot instance
    bot_prefix = Config().load().get("prefix", "alpha")+" "
    bot_Prefix = bot_prefix.capitalize()
    bot = AlphaBot(
        command_prefix=commands.when_mentioned_or(bot_prefix, bot_Prefix),
        case_insensitive=True,
        logger=log
    )

    @bot.event
    async def on_ready():
        main_id = bot.config.get('main_guild')
        bot.main_guild = bot.get_guild(main_id) or bot.guilds[0]
        log.info('\nActive in these guilds/servers:')
        [log.info(g.name) for g in bot.guilds]
        log.info(f'\nMain guild: {bot.main_guild.name}')
        log.info('\nAlphabot started successfully')
        return True


    bot.run()
    log.info('Alphabot has terminated')

if __name__=="__main__":
    main()
