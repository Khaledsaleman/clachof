import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Bot Configuration
API_TOKEN = '7743419348:AAGfAgO9BfN0ri4upy0Rl_y3p10sMu9axm0'
WEBAPP_URL = 'https://tcoc-frontend.render.com'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    """
    Handles the /start command and sends the Mini App button.
    """
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
    print(f"Starting bot @{(await bot.get_me()).username}...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
