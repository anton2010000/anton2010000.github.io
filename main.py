import asyncio
from aiogram import Bot, Dispatcher, executor
from config import load_config
config = load_config('/workspaces/anton2010000.github.io/.env')
BOT_TOKEN = config.tg_bot.token

loop = asyncio.new_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop)

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)