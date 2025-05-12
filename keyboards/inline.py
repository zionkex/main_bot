from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

from callbacks import BotWorker
from database.models import Bot

def inline_keyboard(bots: list[Bot]):
    keyboard = InlineKeyboardBuilder()
    for bot in bots:
        keyboard.add(InlineKeyboardButton(text=bot.name,
                                           callback_data=BotWorker(action="get_info",bot_username=bot.nickname, type=bot.type).pack()))
    return keyboard.adjust(1).as_markup()

def inline_keyboard_workerbot(bot_username: str, user_id: int,bot_type):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Перейти в бота",url=f"https://t.me/{bot_username}?start={user_id}")
    keyboard.button(text="Скрыть реф.ссылку",callback_data=BotWorker(action="hide_ref_link",bot_username=bot_username))
    return keyboard.as_markup()
