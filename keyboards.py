from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from config import load_config
config = load_config('.env')
WEBAPP_URL = config.tg_bot.webapp_url

web_app = WebAppInfo(url=WEBAPP_URL)

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Site", web_app=web_app)]
    ],
    resize_keyboard=True
)

cb = CallbackData('btn', 'action')
key = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton('Pay', callback_data='btn:buy')]]
)