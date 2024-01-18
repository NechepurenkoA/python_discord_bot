import logging
import random

from disnake.ext import commands


class UsefulCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Useful commands loaded.')

    @commands.slash_command(name='random',
                            description='Gives you a random number from ... '
                                        'to ...',)
    async def random_command(self, ctx,
                             first_num: int = commands.Param(
                               name='1st-number',
                               description='First number',
                               default=1,
                             ),
                             second_num: int = commands.Param(
                                 name='2nd-number',
                                 description='Second number',
                                 default=2,
                             )) -> None:
        """Command for getting a random number."""
        if first_num < 0 or second_num < 0:
            await ctx.send(content='Доступны только положительные числа.',
                           ephemeral=True)
        elif first_num > second_num:
            await ctx.send(content='1-е число должно быть меньше 2-го.',
                           ephemeral=True)
        elif first_num == second_num:
            await ctx.send(content='Это не имеет никакого смысла.',
                           ephemeral=True)
        else:
            try:
                await ctx.send(
                    content=f'Вот твоё число - '
                            f'{random.randint(first_num, second_num)}'
                )
            except Exception as error:
                logging.error(f'Произошла ошибка: "{error}"')
                await ctx.send(content='Произошла ошибка. '
                                       'Повторите попытку позже.',
                               ephemeral=True)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(UsefulCommands(bot))
