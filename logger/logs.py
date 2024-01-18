import logging as log_config

log_config.basicConfig(
    level=log_config.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        log_config.FileHandler('bot.log', encoding='utf-8'),
        log_config.StreamHandler(),
    ],
    encoding='utf-8'
)
