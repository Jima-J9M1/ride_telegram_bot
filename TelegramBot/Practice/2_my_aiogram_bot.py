import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold


TOKEN = "6510716903:AAEZz8zn9qxot8qnbaWt4SI_AmS8_cOJ2_Y"

my_router = Router()

@my_router.message(Command('shop'))
async def message_handler(message:Message)->None:
    await message.answer("Hello Wolrd")

@my_router.message(Command('command1'))
async def message_handler_c1(message:Message)->None:
    await message.answer("command1 is running")

@my_router.edited_message()
async def edited_message_handler(edited_message: types.Message) -> any:
    edited_message.answer("Edited message")
    pass

async def main() -> None:
    dp = Dispatcher()
    bot = Bot(TOKEN, parse_mode = ParseMode.HTML)
    
    dp.include_router(my_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())