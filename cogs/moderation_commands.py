import logging

import disnake
from disnake.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.slash_command(name='kick',
                            description='Kick user from the server')
    async def kick(self, ctx,
                   member: disnake.Member = commands.Param(
                      name='user',
                      description='The user to kick'
                   ),
                   *, reason: str = commands.Param(
                      name='reason',
                      description='Reason why you are '
                                  'kicking the user',
                      default='No reason given'
                   )) -> None:
        """Kick a member."""
        if not reason:
            reason = 'No reason was given.'
        try:
            await member.kick(reason=reason)
            logging.info(f'{member} was kicked. Who kicked: {ctx.user}')
            await ctx.send(f'Пользователь {member} был кикнут! '
                           f'Причина: {reason}')
        except Exception as error:
            logging.error(f'Произошла ошибка у {ctx.user}! Ошибка: {error}')
            await ctx.reply(f'Произошла ошибка! Ошибка: {error}')

    # сделать очистку сообщений по времени (wip)

    @commands.has_permissions(ban_members=True)
    @commands.slash_command(name='ban',
                            description='Ban user from the server',)
    async def ban(self, ctx,
                  member: disnake.Member = commands.Param(
                      name='user',
                      description='The user to ban'
                  ),
                  *, reason: str = commands.Param(
                      name='reason',
                      description='Reason why you are '
                                  'banning the user',
                      default='No reason given'
                  )) -> None:
        """Ban a user."""
        try:
            await member.ban(reason=reason)
            logging.info(f'{member} was banned. Who banned: {ctx.user}')
            await ctx.send(f'Пользователь {member} был забанен! '
                           f'Причина: {reason}')
        except Exception as error:
            logging.error(f'Произошла ошибка у {ctx.user}! Ошибка: {error}')
            await ctx.user.reply(f'Произошла ошибка! Ошибка: {error}')

    @commands.has_permissions(ban_members=True)
    @commands.slash_command(name='unban',
                            description='Unban user')
    async def unban(self, ctx,
                    member: disnake.User = commands.Param(
                        name='user',
                        description='The user to unban',),
                    *, reason: str = commands.Param(
                        name='reason',
                        description='Reason why you are '
                                    'unbanning the user',
                        default='No reason given'
                    )) -> None:
        """Unban a user."""
        try:
            await ctx.guild.unban(member, reason=reason)
            logging.info(f'{member} was unbanned. Who unbanned: {ctx.user}')
            await ctx.send(f'Пользователь {member} был разбанен!')
        except Exception as error:
            logging.error(f'Произошла ошибка у {ctx.user}! Ошибка: {error}')
            await ctx.send(f'Произошла ошибка! Ошибка: {error}', )

    @commands.has_permissions(manage_messages=True)
    @commands.slash_command(name='clear',
                            description='Delete any amount of messages')
    async def clear(self, ctx,
                    amount: int = commands.Param(
                        name='amout',
                        description='Amount of messages to clear',
                        default=1
                    )):
        """Clear chat."""
        try:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'Удалено {amount} сообщений!', delete_after=5)
        except Exception as error:
            logging.error(f'Произошла ошибка у {ctx.user}! Ошибка: {error}')
            await ctx.send(f'Произошла ошибка! Ошибка: {error}')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Moderation(bot))
