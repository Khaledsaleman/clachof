import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = '7743419348:AAGfAgO9BfN0ri4upy0Rl_y3p10sMu9axm0'
WEBAPP_URL = 'https://tcoc-frontend.render.com'

logging.basicConfig(level=logging.INFO)

# Using aiogram 3.x style
from aiogram import F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Play TCOC ⚔️", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])

    await message.reply(
        "Welcome to **TON Clash of Clans**! 🏰\n\n"
        "Strategic warfare meets the TON blockchain. Build, attack, and earn rewards in the most addictive strategy game on Telegram.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
