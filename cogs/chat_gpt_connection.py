import asyncio
import logging
import datetime

import disnake
from disnake.ext import commands

from utils import parse_for_chat_gpt_answer


CHAT_GPT_LINK = 'https://chat-gpt.org/chat'


class ChatGPT(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ChatGPT loaded.')

    @commands.Cog.listener()
    async def on_message(self, message):
        """
            Считываем сообщение из чата бота и
            отправляем ответ на запрос.
        """
        channel = disnake.utils.get(message.guild.channels, name='ботиха-гпт')
        if message.content.startswith('gpt') and message.channel == channel:
            await message.reply(content='Соблюдайте регистр, '
                                        'пишите запрос начиная с GPT')
            return
        if message.content.startswith('GPT') and message.channel == channel:
            role = disnake.utils.get(message.guild.roles, name='chat_gpt')
            if role in message.author.roles:
                try:
                    answer: str = parse_for_chat_gpt_answer(message)
                    if len(answer) < 1024:
                        embed = disnake.Embed(
                            title="Ваш ответ на вопрос:",
                            description=f'{message.content}',
                            color=disnake.Colour.green(),
                            timestamp=datetime.datetime.now(),
                        )
                        embed.set_author(
                            name='Chat GPT',
                            icon_url='https://imgur.com/WzrDOB0.png'
                        )
                        embed.add_field(name='Ответ:', value=answer)
                        await message.reply(embed=embed)
                        await asyncio.sleep(60)
                    else:
                        embed = disnake.Embed(
                            title="Ваш ответ на вопрос:",
                            description=f'{message.content}',
                            color=disnake.Colour.green(),
                            timestamp=datetime.datetime.now(),
                        )
                        embed.set_author(
                            name='Chat GPT',
                            icon_url='https://imgur.com/WzrDOB0.png'
                        )
                        embed.add_field(
                            name='Ответ:',
                            value=f'''
                            Ответ ИИ превысил 1024 символа, к сожалению
                            вопрос придётся задать тут -> {CHAT_GPT_LINK}
                            '''
                            )
                        await message.reply(embed=embed)
                        await asyncio.sleep(60)
                except Exception as error:
                    logging.warning(f'Появилась ошибка: {error}')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ChatGPT(bot))
