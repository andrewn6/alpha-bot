from discord.ext import commands


class AlphaCtx(commands.Context):
    @property
    def session(self):
        return self.bot.session
