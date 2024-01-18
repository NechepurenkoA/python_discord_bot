import locale

from bot import bot, settings
from logger import log_config

logger = log_config.getLogger(__name__)
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))


@bot.event
async def on_ready():
    print('Bot is running!')


def main():
    bot.run(settings['token'])


if __name__ == '__main__':
    main()