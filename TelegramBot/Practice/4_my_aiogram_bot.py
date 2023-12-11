import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, Router, types,F, Router, html
from aiogram.enums import ParseMode
from aiogram.methods.send_message import SendMessage
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
    )



from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = "6510716903:AAEZz8zn9qxot8qnbaWt4SI_AmS8_cOJ2_Y"


dp = Dispatcher()
bot = Bot(token=TOKEN)
form_router = Router()

class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()



@form_router.message(Command('start'))
async def command_start_handler(message:Message, state:FSMContext):
    await state.set_state(Form.name)
    await message.answer(
        "Hi there! What's your name?",
        reply_markup = ReplyKeyboardRemove(),
    ) 
    

@form_router.message(Form.name)
async def process_name(message:Message, state:FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.like_bots)
    # data = await state.get_data()
    # print(data.name)
    await message.answer(
        f"Nice to meet you, {html.quote(message.text)}!\n Did you like to write bots?",
        reply_markup=ReplyKeyboardMarkup(

            keyboard=[

                [

                    KeyboardButton(text="Yes"),

                    KeyboardButton(text="No"),

                ]

            ],

            resize_keyboard=True,

        ),
    )


@form_router.message(Form.like_bots, F.text.casefold() == "no")
async def command_handle_nobots(message:Message, state:FSMContext):
    data  = await state.get_data()
    # await bot(SendMessage(chat_id=message.chat.id, message_id=message.message_id, reply_markup=ReplyKeyboardRemove()))
    await state.clear()
    
    await message.answer(
        'Not bad not terrible.\nSee you soon.',
        reply_markup = ReplyKeyboardRemove()
    )


    # await show_summary(message=message, data=data, positive=False)





# @form_router.message(Command('register'))
# async def command_register_handler(message:Message):

# @form_router.message(Command('cancel'))
# async def command_cancel_handler(message:Message):

    
async def main():
    bot = Bot(token=TOKEN, parse_mode = ParseMode.HTML)
    dp = Dispatcher() 
    dp.include_router(form_router)

    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())