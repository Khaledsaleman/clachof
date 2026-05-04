import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = 'YOUR_BOT_TOKEN'
WEBAPP_URL = 'https://tcoc-frontend.render.com'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text="Play TCOC ⚔️",
        web_app=types.WebAppInfo(url=WEBAPP_URL)
    ))

    await message.reply(
        "Welcome to **TON Clash of Clans**! 🏰\n\n"
        "Strategic warfare meets the TON blockchain. Build, attack, and earn rewards in the most addictive strategy game on Telegram.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
