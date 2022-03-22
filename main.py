import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # loads virtual env for tokens

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    cog_folder = os.listdir('./cogs')
    for file_name in cog_folder:
        if file_name.endswith('.py'):
            client.load_extension(f'cogs.{file_name[:-3]}')
    activity = discord.Game('`help', type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


if __name__ == '__main__':
    client.run(os.getenv('DISCORD_TOKEN'))
