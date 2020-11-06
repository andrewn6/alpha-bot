"""This is a cog for a discord.py bot.
It drops random cheese for people to pick up
"""
from collections import defaultdict
from datetime import datetime as dt
from discord import Activity, DMChannel, Client, Message
from discord.ext import commands
import asyncio
import json
import random


class Cheese(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, client):
        self.client = client
        self.cheese_emoji = u"\U0001F9C0"
        self.thumbup_emoji = u"\U0001F44D"
        self.thumbdown_emoji = u"\U0001F44E"
        self.last_cheese = dt.utcnow()
        # TODO: add a check if this exists if not create it
        self.cheese_weight = (
            100 - self.client.config.get("cheese_weight", 50), 100)
        self.cooldown = 30
        self.store_file = 'cheese_store.json'
        self.scores = self.load_memory()
        random.seed()

    async def save_memory(self):
        try:
            with open(self.store_file, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f)
        except Exception as e:
            self.client.log.warning(f"Unable to save cheese memory! : {e}")

    def load_memory(self):
        try:
            with open(self.store_file, 'r', encoding='utf-8') as f:
                return defaultdict(int, json.load(f))
        except Exception as e:
            self.client.log.warning(
                f"Unable to load cheese memory from file! : {e}")
            return defaultdict(int)

    async def add_cheese(self, client: Client, msg: Message):
        message = 'A wild cheese appeared!'
        await msg.channel.send(message)
        await msg.add_reaction(self.cheese_emoji)
        await msg.channel.send(await self.check_reaction(client))

    async def check_reaction(self, client: Client):
        def check(reaction, user):
            return not user.bot and str(reaction.emoji) == self.cheese_emoji
        message_store = ""
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            self.scores[user.id] += 1
            await self.save_memory()
        except asyncio.TimeoutError:
            message_store += self.thumbdown_emoji
            return message_store
        else:
            message_store += f"{self.thumbup_emoji}\n"
            message_store += "Cheeses collected:\n"
            message = []
            for k, v in self.scores.items():
                message.append(f"{client.get_user(k)}: {v}")
            message_store += "\n".join(message)
            return message_store

    @commands.Cog.listener()
    async def on_message(self, msg: Message):
        if msg.author.bot or isinstance(msg.channel, DMChannel):
            # Ignore DM or mesage from a bot
            return
        client = self.client
        chance_result = random.choices(
            [0, 1], cum_weights=self.cheese_weight)[0]
        client.log.debug(f"{chance_result=}")
        if chance_result:
            if (dt.utcnow() - self.last_cheese).total_seconds() < self.cooldown:
                return
            await self.add_cheese(client, msg)
            self.last_cheese = dt.utcnow()


def setup(client):
    """This is called when the cog is loaded via load_extension"""
    client.add_cog(Cheese(client))
