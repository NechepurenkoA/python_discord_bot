import logging
import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

from utils import get_token

load_dotenv()

EXTENSION_CHOICES: list[:str] = ['moderation_commands',
                                 'useful_commands',
                                 'hentai_commands',
                                 'chat_gpt_connection',
                                 'reddit_connection',
                                 'music_commands',
                                 'all'
                                 ]

TOKEN: str = get_token('DISCORD_BOT_TOKEN')
SERVER_ID: int = int(get_token('SERVER_ID'))
BOT_ID: int = int(get_token('BOT_ID'))

settings = {
    'token': TOKEN,
    'id': BOT_ID,
    'command_prefix': '!'
}

bot = commands.Bot(intents=disnake.Intents.all(),
                   help_command=None,
                   test_guilds=[SERVER_ID, ],
                   command_prefix=settings['command_prefix'])
bot.remove_command('kick')


@bot.slash_command(name='load', description='Load a cog')
async def load(ctx, extension: str = commands.Param(
                      name='extension',
                      description='Cog to load',
                      choices=EXTENSION_CHOICES
                   )):
    """Loading cog."""
    if ctx.author.id == 345990695435108355 or \
            ctx.author.id == 345990609292623887:
        try:
            if extension == 'all':
                for ext in EXTENSION_CHOICES[:-1]:
                    bot.load_extension(f'cogs.{ext}')
                await ctx.send(
                    content=f'All extensions are loaded successfully.',
                    ephemeral=True
                )
            else:
                bot.load_extension(f'cogs.{extension}')
                await ctx.send(
                    content=f'Cog "{extension}" is loaded successfully.',
                    ephemeral=True
                )
        except Exception as error:
            logging.critical(f'The error occurred! '
                             f'Loading of the "{extension}" was failed! '
                             f'Error:{error}')
            await ctx.send(content=f'The error occurred! '
                                   f'Loading of the "{extension}" was failed! '
                                   f'Error:{error}',
                           ephemeral=True)
    else:
        await ctx.send(content='У вас недостаточно прав!',
                       ephemeral=True)


@bot.slash_command(name='unload', description='Unload cog if needed')
async def unload(ctx, extension: str = commands.Param(
                      name='extension',
                      description='Cog to unload',
                      choices=EXTENSION_CHOICES
                   )):
    """Unloading cog."""
    if ctx.author.id == 345990695435108355 or \
            ctx.author.id == 345990609292623887:
        try:
            if extension == 'all':
                for ext in EXTENSION_CHOICES[:-1]:
                    bot.unload_extension(f'cogs.{ext}')
                await ctx.send(
                    content=f'All extensions are unloaded successfully.',
                    ephemeral=True
                )
            else:
                bot.unload_extension(f'cogs.{extension}')
                await ctx.send(
                    content=f'Cog "{extension}" is unloaded successfully.',
                    ephemeral=True
                )
        except Exception as error:
            logging.critical(f'The error occurred! '
                             f'Unloading of the "{extension}" was failed! '
                             f'Error:{error}')
            await ctx.send(content=f'The error occurred! '
                                   f'Unloading of the "{extension}" was failed! '
                                   f'Error:{error}',
                           ephemeral=True)
    else:
        await ctx.send(content='У вас недостаточно прав!',
                       ephemeral=True)


@bot.slash_command(name='reload', description='Reload cog if needed')
async def reload(ctx, extension: str = commands.Param(
                      name='extension',
                      description='Cog to reload',
                      choices=EXTENSION_CHOICES
                   )):
    """Reloading cog."""
    if ctx.author.id == 345990695435108355 or \
            ctx.author.id == 345990609292623887:
        try:
            if extension == 'all':
                for ext in EXTENSION_CHOICES[:-1]:
                    bot.unload_extension(f'cogs.{ext}')
                    bot.load_extension(f'cogs.{ext}')
                await ctx.send(
                    content=f'All extensions are reloaded successfully.',
                    ephemeral=True
                )
            else:
                bot.unload_extension(f'cogs.{extension}')
                bot.load_extension(f'cogs.{extension}')
                await ctx.send(content=f'Cog "{extension}" is reloaded.',
                               ephemeral=True
                               )
        except Exception as error:
            logging.critical(f'The error occurred! '
                             f'Reloading of the "{extension}" was failed! '
                             f'Error: {error}')
            await ctx.send(content=f'The error occurred! '
                                   f'Reloading of the "{extension}" was failed! '
                                   f'Error: {error}',
                           ephemeral=True)
    else:
        await ctx.send(content='У вас недостаточно прав!',
                       ephemeral=True)
