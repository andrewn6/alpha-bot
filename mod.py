import discord
from discord.ext import commands
from discord import utils

class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason)
        await ctx.send(f"{user} has been banned for {reason}")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        await ctx.send(f"{user} has been kicked for {reason}")


    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def warn(self, ctx, user: discord.Member, reason=None):
        await user.warn(reason=reason)
        await ctx.send(f'{user} has been warned for {reason}')
    
    
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def mute(self, ctx, user: discord.Member, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        user = ctx.message.author
        await user.add_roles(role)
        await ctx.send(f"{user} has been muted for {reason}")

    
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Moderation", description="Moderation commands for admins/mods")
        embed.add_field(name="ban", value="Ban a member. alpha ban [user] (reason)", inline=False)
        embed.add_field(name="clean", value="Clean up responses/messages alpha clean (count)", inline=False)
        embed.add_field(name="clearnotes", value="Delete all notes about a member alpha clearnotes [user]", inline=False)
        embed.add_field(name="deafen", value="Defean a member alpha deafen [user] (reason)")
        embed.add_field(name="delnote", value="Delete a singl note about a member alpha delnot [user] [note ID]", inline=False)
        embed.add_field(name="delwarn", value="Clear a single warning from a member. alpha del warn [warning ID]", inline=False)
        embed.add_field(name="diagnose", value="Diagnose any command or module in the bot to determine if there are any problems")
      
        # At editnote command
        embed.add_field(name)
def setup(bot): 
    bot.add_cog(Mod)