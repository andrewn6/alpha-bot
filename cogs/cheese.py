"""This is a cog for a discord.py bot.
It drops random cheese for people to pick up
"""
import random
from datetime import datetime as dt
from discord.ext import commands
from discord import Activity, DMChannel


class Cheese(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, client):
        self.client = client
        self.last_cheese = dt.utcnow()
        self.chance = 1
        self.cooldown = 30
        random.seed()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if isinstance(msg.channel, DMChannel):
            # Ignore DM
            return
        if random.randint(1, 100 // self.chance) == 1:
            if (dt.utcnow() - self.last_cheese).total_seconds() < self.cooldown:
                return

            cheese = 'A random cheese appeared!'
            await msg.add_reaction('🧀')
            await msg.channel.send("A wild cheese appeared")
            self.last_cheese = dt.utcnow()


def setup(client):
    """This is called when the cog is loaded via load_extension"""
    client.add_cog(Cheese(client))

