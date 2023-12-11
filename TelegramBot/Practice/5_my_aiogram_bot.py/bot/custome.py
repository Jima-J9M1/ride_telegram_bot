from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from  aiogram.utils.keyboard import ReplyKeyboardBuilder


builder = ReplyKeyboardBuilder()
MenuButtonDriver = ReplyKeyboardBuilder()
MenuButtonPassenger = ReplyKeyboardBuilder()
startButton = ReplyKeyboardBuilder()
registerButton = ReplyKeyboardBuilder()
updateButtonsForDriver = ReplyKeyboardBuilder()
updateButtonsForPassenger = ReplyKeyboardBuilder()


# Register Button
#########################################
registerButton.button(text='Register')
#########################################
# Start Button
startButton.button(text=f"/start")

# Menu Button Passenger
############################################
MenuButtonPassenger.button(text=f"Book Ride")
MenuButtonPassenger.button(text=f"Update Profile")
MenuButtonPassenger.button(text=f"Rate Driver")
MenuButtonPassenger.button(text=f"Cancel")

MenuButtonPassenger.adjust(1,2)

#############################################


# Menu Button Driver
############################################
MenuButtonDriver.button(text=f"Update Profile")
MenuButtonDriver.button(text=f"Rate Passenger")
MenuButtonDriver.button(text=f'Change Status')
MenuButtonDriver.button(text=f"Cancel")

MenuButtonDriver.adjust(2)
#############################################


# Update Button for Driver
#############################################
updateButtonsForPassenger.button(text="Name")
updateButtonsForPassenger.button(text="Role")
updateButtonsForPassenger.button(text="Done")
updateButtonsForPassenger.adjust(2)
#############################################

# Update Button for Driver
#############################################
updateButtonsForDriver.button(text="Name")
updateButtonsForDriver.button(text="role")
updateButtonsForDriver.button(text="Done")
updateButtonsForDriver.adjust(2)
#############################################
# for index in range(1, 11):
builder.button(text=f"Share Contact",request_contact=True)

builder.adjust(3, 2)




replyBuilder = ReplyKeyboardBuilder()
# inLineBuilder = InlineKeyboardBuilder()

# inLineBuilder.button(text=f"Share")
# # request_contact=True

# builder.button(text=f"Share Contact",request_contact=True)
replyBuilder.button(text=f"Driver")
replyBuilder.button(text=f"Passenger")

# # replyBuilder.adjust(4, 1,3)
# # builder.row("3")
