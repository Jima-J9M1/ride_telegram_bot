import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# TOKEN = getenv('BOT_TOKEN')
TOKEN = "6510716903:AAEZz8zn9qxot8qnbaWt4SI_AmS8_cOJ2_Y"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello Father Bot")


@dp.message_handler(Command('shop'))
async def command_shop_handler(message: Message) -> None:
    await message.answer("Welcome to jshopify, shop whatever you want :)")

# Add another command handler
@dp.message_handler(Command('help'))
async def command_help_handler(message: Message) -> None:
    await message.answer("This is a help message. You can add more information here.")

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except:
        await message.answer('Nice Try')

async def main() -> None:
    # Remove the unnecessary bot instantiation in the main function
    await dp.start_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
