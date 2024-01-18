import asyncio
import logging

import disnake
from disnake.ext import commands

from utils import get_submission_embed

user_agent: str = 'Scraper 1.0 by /u/EncodedBatiskaf'


class Reddit(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:

        self.bot = bot
        bot.loop.create_task(Reddit.auto_meme(self))

    async def auto_meme(self) -> None:
        try:
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                channel = self.bot.get_channel(1038534786194624612)
                embed: disnake.Embed = await get_submission_embed(user_agent)
                await channel.send(embed=embed)
                await asyncio.sleep(600)
        except Exception as error:
            logging.critical(f'Ошибка: {error}')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Reddit cog loaded.')

    @commands.slash_command(name='meme',
                            description='bot will send you a random meme')
    async def reddit_meme(self, ctx) -> None:
        """Command for Reddit memes."""
        await ctx.response.defer(with_message=True)
        embed: disnake.Embed = await get_submission_embed(user_agent)
        await ctx.edit_original_message(content=' ', embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Reddit(bot))
