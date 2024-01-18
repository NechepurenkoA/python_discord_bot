import datetime
import os
from http import HTTPStatus
import logging
import random


import asyncpraw
import disnake
from dotenv import load_dotenv
import openai
import requests

from exceptions import APIException

load_dotenv()
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')


def get_token(key: str) -> str:
    """Проверяем наличие токена."""
    token: str | None = os.getenv(key)
    if token != "" or None:
        return token
    raise APIException(f'Не передан токен {key}!')


def parse_for_image(url: str) -> dict:
    """Берем картинку с API."""
    response = requests.get(url)
    if response.status_code == HTTPStatus.OK:
        return response.json()
    raise APIException('Не удалось установить связь с nekos.fun!')


def parse_for_chat_gpt_answer(message: disnake.Message) -> str:
    openai.api_key = get_token('CHAT_GPT_API_KEY')
    if not message:
        messages = [
            {'role': 'user', 'content': 'Ты крут'},
        ]
    messages = [
        {'role': 'user',
         'content': message.content.split('GPT')[1]
         },
    ]
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    return answer


async def get_submission_embed(user_agent: str) -> disnake.Embed:
    all_subs: list[asyncpraw.reddit.Submission] = []
    async with asyncpraw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=user_agent
    ) as reddit:
        try:
            subreddit: asyncpraw.reddit.Subreddit = await reddit.subreddit('memes', fetch=True)
            async for submission in subreddit.hot(limit=50):
                all_subs.append(submission)
            random_sub: asyncpraw.reddit.Submission = random.choice(all_subs)
            embed = disnake.Embed(
                title=random_sub.title,
                color=disnake.Colour.orange(),
                timestamp=datetime.datetime.now(),
            )
            embed.set_author(
                name='Reddit',
                icon_url='https://imgur.com/keTBzSb.png'
            )
            embed.set_image(url=random_sub.url)
            return embed
        except Exception as error:
            logging.critical(f'Ошибка {error}')
