import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.utils.markdown import hbold


from aiogram.utils.callback_query import CallbackQuery
from aiogram.utils.exceptions import CantParseUpdates

# logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "6510716903:AAEZz8zn9qxot8qnbaWt4SI_AmS8_cOJ2_Y"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def process_update(update):
    try:
        await dp.dispatch(update)
    except CantParseUpdates as e:
        logging.error(f"CantParseUpdates: {e}")
        return

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    await message.reply(message.text)

@dp.callback_query_handler()
async def callback(callback_query: CallbackQuery):
    if callback_query.data == "button1":
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer("Button 1 clicked")
    elif callback_query.data == "button2":
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer("Button 2 clicked")

async def main():
    while True:
        try:
            update = await bot.get_updates()
            await process_update(update)
        except (asyncio.TimeoutError, ConnectionError) as e:
            logging.error(f"Error while receiving updates: {e}")
            await asyncio.sleep(3)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())