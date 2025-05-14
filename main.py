from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

import asyncio
import logging
import sys
from database.engine import db
from middlewars.db import DataBaseSession
from handlers import main_router
from config import settings

TOKEN = settings.TOKEN

dp = Dispatcher()
dp.update.middleware (DataBaseSession(session_pool=db.sessionmaker))
dp.include_router(main_router)


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
