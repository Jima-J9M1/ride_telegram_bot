import asyncio
import logging
import sys
from aiogram import Dispatcher
from bot_instance import bot
from bot.handlers.user_handler import user_router


def register_router(dp:Dispatcher) -> None:
    dp.include_router(user_router)
    



async def main() -> None:
    dp = Dispatcher()
    

    register_router(dp)
    await dp.start_polling(bot)

    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    

    
