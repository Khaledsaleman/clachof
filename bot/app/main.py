import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Bot Token
API_TOKEN = '7743419348:AAGfAgO9BfN0ri4upy0Rl_y3p10sMu9axm0'
# Update this to your real URL after deployment
WEBAPP_URL = 'https://tcoc-frontend.render.com'

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    """
    Handles /start and sends a welcome message with a Web App button.
    """
    logging.info(f"Received /start from user {message.from_user.id}")

    # Using HTML for better stability in Telegram
    welcome_text = (
        "<b>Welcome to TON Clash of Clans!</b> 🏰\n\n"
        "The ultimate strategy war game on Telegram. Build your village, "
        "train your heroes, and earn TON rewards in real-time PvP battles.\n\n"
        "Click the button below to start your journey! 👇"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Launch Game ⚔️", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])

    try:
        await message.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")
        logging.info("Sent welcome message successfully.")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

async def main():
    me = await bot.get_me()
    print(f"Bot @{me.username} is now ONLINE.")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot is offline.")
