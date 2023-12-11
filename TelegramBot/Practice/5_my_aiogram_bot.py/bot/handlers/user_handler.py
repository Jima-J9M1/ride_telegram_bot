from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ContentType

)


from aiogram.enums import ParseMode

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import contact
from aiogram.types.user import User
from aiogram.utils.markdown import hbold
from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.custome import (
    builder,
    replyBuilder,
    MenuButtonDriver,
    MenuButtonPassenger,
    startButton,
    registerButton,
    updateButtonsForDriver,
    updateButtonsForPassenger
    
    )
from  bot_instance import bot
from config import redis_connect
from .service_handler import register,get_user_by_id, update_profile

user_router = Router()

class Form(StatesGroup):
    name = State()
    contact_info = State()
    role = State()
    register = State()
    update_profile = State()
    edit_name = State()
    edit_role = State()
    edit_done = State()
    book_ride = State()
    location = State()
    long_start = State()
    long_end = State()
    save_booking = State()



@user_router.message(Command('start'))
async def message_handler_c1(message:Message, state:FSMContext)->None:
    user_id = message.from_user.id
    user_key = f"user:{user_id}"

    print(user_id, user_key)

    if not redis_connect.exists(user_key):
        print("Data base Connection")
        await state.set_state(Form.register)
        await message.answer(
            f"Welcome To RIDE WITH ME Service",
            reply_markup=registerButton.as_markup(resize_keyboard=True)
               )
    else:
        user = redis_connect.hgetall(user_key)
        if user['role'] == 'Driver':
            await message.answer(
            ''' 
             🚗 Welcome, Driver! 🚗 \n  
Explore your options as a driver on our platform:\n\n  
   🌐 **Update Your Profile** \n 
   Keep your information current and ensure passengers have the best details about you.\n\n 
   ⭐ **Rate Your Customers**\n 
   Share your experiences by rating your passengers. Help build a respectful community.\n\n 
   🚦 **Change Your Status**\n 
   Toggle your availability easily. Be on or off duty with just a tap.\n\n 
   Drive with us and enjoy a seamless journey! 🛣️''',

 reply_markup=MenuButtonDriver.as_markup(resize_keyboard=True)

)
        else:
            await state.set_state(Form.book_ride)
            await message.answer(
                '''👤 Welcome, Passenger! 👤\n 
Discover the features available for passengers like you:\n\n 
   🌐 **Update Your Profile**\n 
   Maintain accurate details to enhance your experience with our drivers.\n\n 
   ⭐ **Rate Your Drivers**\n 
   Share your feedback by rating your rides. Help improve the quality of our service.\n\n 
🚖 **Book a Ride Service**\n 
   Easily book rides to your destination. Experience hassle-free travel with us!\n\n 
Embark on a comfortable journey with our reliable drivers! 🌟
                ''',
    reply_markup=MenuButtonPassenger.as_markup(resize_keyboard=True)
    
            )
    # else:
    # data = await state.get_data()
    #     if(data['role'] == "Passenger"):
    #         await message.answer(
    #             f"Wellcom To J-Ride service.\n Book Ride",
    #              reply_markup = MenuButtonPassenger.as_markup(resize_keyboard=True)
    #         )
    #     else:
    #         await message.answer(
    #             f"Wellcom To Driver:{data['name']}",
    #              reply_markup = MenuButtonDriver.as_markup(resize_keyboard=True)
    #         )


    # else:


@user_router.message(Form.register, F.text.casefold() == "register")
async def register_user(message:Message, state:FSMContext):
    await state.set_state(Form.name)

    await message.answer(
        f"Hi there What is your name?",
        reply_markup = ReplyKeyboardRemove()
        )

@user_router.message(Form.name)
async def user_reg(message:Message, state:FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.contact_info)
    await message.answer(
        f"Hi {hbold(message.text)}, Enter your phone number",
        reply_markup = builder.as_markup(resize_keyboard=True)
    )


@user_router.message(Form.contact_info)
async def user_choose_role(message:Message, state:FSMContext) -> None:
    name = ""
    phone = ""
    
    print(message.contact)
    if message.contact and message.contact.phone_number:
        phone = message.contact.phone_number
        name = message.contact.first_name

    await state.update_data(name=name,contact_info=phone)
    await state.set_state(Form.role)

    data = await state.get_data()
    print(data)
    
    
    await message.answer(
        f"You are almost done, {data['name']}!\n What is your role?",
        reply_markup = replyBuilder.as_markup(resize_keyboard=True)
    )



@user_router.message(Form.role, F.text.casefold() == "driver")
async def command_handle_nobots(message:Message, state:FSMContext):
    await state.update_data(role=message.text)
    data  = await state.get_data()
    
    await register(message.from_user.id, data)

    await message.answer(
        f"Congrats! {data['name']}.\n Registeration Successful.\n Start to use the services",
        reply_markup = startButton.as_markup(resize_keyboard=True)
    )

@user_router.message(F.text.casefold() == "cancel")
async def command_handle_nobots(message:Message, state:FSMContext):
    await state.clear()
    
    await message.answer(
        f"Welcome back",
        reply_markup = startButton.as_markup(resize_keyboard=True)
    )



@user_router.message(Form.role, F.text.casefold() == "passenger")
async def command_handle_nobots(message:Message, state:FSMContext):
    await state.update_data(role=message.text)
    data  = await state.get_data()
    
    await register(message.from_user.id, data)

    await message.answer(
        f"Congrats! {data['name']}.\n Registeration Successful.\n Start to use the services",
        reply_markup = startButton.as_markup(resize_keyboard=True)
    )


@user_router.message(F.text.casefold() == 'update profile')
async def handle_update_user(message:Message, state:FSMContext):
    user_id = message.from_user.id
    user_key = f"user:{user_id}"
    await state.set_state(Form.update_profile)
    user = redis_connect.hgetall(user_key)

    if user['role'] == "Driver":
        await message.answer(
            f"Name:{user['name']}\n Role:{user['role']}\n Status:{user['status']}",
            reply_markup = updateButtonsForDriver.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
    """
   👤 **Update Your Passenger Profile**

    Hello, Passenger! Enhance your journey by keeping your profile information current. Here's what you can update:

""" +
     f"Name:{user['name']}\nRole:{user['role']}\n",
            reply_markup = updateButtonsForPassenger.as_markup(resize_keyboard=True)
        )

@user_router.message(Form.update_profile)
async def update_user(message:Message, state:FSMContext):
    user_id = message.from_user.id
    user = get_user_by_id(user_id)
    user_key = f"user:{user_id}"
    user = redis_connect.hgetall(user_key)

    if message.text.casefold() == 'name':
        await state.set_state(Form.edit_name)

        await message.answer(
            "Enter your new name: ",
            reply_markup=ReplyKeyboardRemove()
        )

    elif message.text.casefold() == "role":
        await state.set_state(Form.edit_role)

        if user['role'] == "Driver":
            
            await message.answer(
                f"Now your are {user['role']}\n\nAre your sure you want to be Passenger",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                 keyboard=[
                    [KeyboardButton(text="Yes")],
                    [KeyboardButton(text="No")]
                ]))
        else:
            await message.answer(
                f"Now your are {user['role']}\n\n Are your sure you want to be Driver",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                 keyboard=[
                    [KeyboardButton(text="Yes")],
                    [KeyboardButton(text="No")]
                ]))
            
    else:
        await state.set_state(Form.edit_done)

        await message.answer(
                f"Are your sure you want to update your information",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                 keyboard=[
                    [KeyboardButton(text="Yes")],
                    [KeyboardButton(text="No")]
                ]))


@user_router.message(Form.edit_name)
async def change_user_name(message:Message, state:FSMContext):
    await state.update_data(edit_name=message.text)
    user = get_user_by_id(message.from_user.id)
    await state.set_state(Form.update_profile)
    
    if user['role'] == "Driver":
        await message.answer(
            f"Continue",
            reply_markup=updateButtonsForDriver.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
            f"Continue",
            reply_markup=updateButtonsForPassenger.as_markup(resize_keyboard=True)
        )

@user_router.message(Form.edit_role, F.text.casefold() == "yes")
async def change_user_role(message:Message, state:FSMContext):
    user = get_user_by_id(message.from_user.id)
    data = await state.get_data()
    
    await state.set_state(Form.update_profile)
    
    if user['role'] == 'Driver':
        await state.update_data(edit_role="Passenger")
    else:
        await state.update_data(edit_role="Driver")

    if user['role'] == "Driver":
        await message.answer(
            f"Continue",
            reply_markup=updateButtonsForDriver.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
            f"Continue",
            reply_markup=updateButtonsForPassenger.as_markup(resize_keyboard=True)
        )



    
@user_router.message(Form.edit_role, F.text.casefold() == "no")
async def redirect_to_updateProfile(message:Message, state:FSMContext):
    user = get_user_by_id(message.from_user.id)
    
    await state.set_state(Form.update_profile)
    
    if user['role'] == 'Driver':
        await state.update_data(edit_role="Passenger")
    else:
        await state.update_data(edit_role="Driver")

    if user['role'] == "Driver":
        await message.answer(
            f"Continue",
            reply_markup=updateButtonsForDriver.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
            f"Continue",
            reply_markup=updateButtonsForPassenger.as_markup(resize_keyboard=True)
        )



    
@user_router.message(Form.edit_done, F.text.casefold() == "yes")
async def finish_update(message:Message, state:FSMContext):
    data = await state.get_data()
    user = get_user_by_id(message.from_user.id)
    
    if 'edit_name' in data:
        name = data['edit_name']
    else:
        name = user['name']

    if 'edit_role' in data:
        role = data['edit_role']
    else:
        role = user['role']

    update_data = {
        'name':name,
        "role":role
    }

    update_profile(message.from_user.id, update_data)

    await message.answer(
            f"Successful Updated!",
            reply_markup=startButton.as_markup(resize_keyboard=True)
        )
    


@user_router.message(Form.book_ride, F.text.casefold() == 'book ride')
async def handle_booking(message:Message, state:FSMContext):
    await state.set_state(Form.location)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
        keyboard=[[KeyboardButton(text="Share Locaiton", request_location=True)]])
    await message.answer("please share you location:", reply_markup=keyboard)


@user_router.message(Form.location)
async def destination(message:Message, state:FSMContext):
    await state.update_data(long_start = message.location.longitude)
    print(message.location.longitude)
    await state.set_state(Form.long_end)
    await message.answer("please share your destination:",
                         reply_markup = ReplyKeyboardRemove()
                         )


@user_router.message(Form.long_end)
async def update_dest(message:Message, state:FSMContext):
    await state.update_data(long_end=message.text)
    menu_Passenger = ReplyKeyboardMarkup(resize_keyboard=True,
        keyboard=[
                    [KeyboardButton(text="Confirm")],
                    [KeyboardButton(text="Cancel")]
                ])
    await message.answer("Please confirm your booking:", reply_markup=menu_Passenger)


@user_router.message(Form)