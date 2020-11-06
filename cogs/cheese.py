"""This is a cog for a discord.py bot.
It drops random cheese for people to pick up
"""
from collections import defaultdict
from datetime import datetime as dt
from discord import Activity, DMChannel
from discord.ext import commands
import random


class Cheese(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, client):
        self.client = client
        self.last_cheese = dt.utcnow()
        self.cheese_weight = (100 - self.client.config.get("cheese_weight", 50), 100)
        self.cooldown = 30
        self.scores = defaultdict(int)
        random.seed()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if isinstance(msg.channel, DMChannel):
            # Ignore DM
            return
        client = self.client
        chance_result = random.choices([0,1], cum_weights=self.cheese_weight)[0]
        client.log.debug(f"{chance_result=}")
        if chance_result:
            #if (dt.utcnow() - self.last_cheese).total_seconds() < self.cooldown:
            #    return
            message = 'A wild cheese appeared!'
            await msg.channel.send(message)
            await msg.add_reaction('🧀')
            def check(reaction, user):
                return not user.bot and str(reaction.emoji) == '🧀'
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                self.scores[user.id] += 1
            except asyncio.TimeoutError:
                await msg.channel.send('👎')
            else:
                await msg.channel.send('👍')
                await msg.channel.send(f"Cheeses collected: {self.scores}")
            self.last_cheese = dt.utcnow()


def setup(client):
    """This is called when the cog is loaded via load_extension"""
    client.add_cog(Cheese(client))

