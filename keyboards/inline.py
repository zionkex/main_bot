from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

from callbacks import BotWorker
from database.models import Bot

def inline_keyboard(bots: list[Bot]):
    keyboard = InlineKeyboardBuilder()
    for bot in bots:
        keyboard.add(InlineKeyboardButton(text=bot.name,
                                           callback_data=BotWorker(action="get_info",bot_username=bot.nickname, type=bot.type).pack()))
    return keyboard.adjust(1).as_markup()

def keyboard_workerbot(bot_username: str, user_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Перейти в бота",url=f"https://t.me/{bot_username}?start={user_id}")
    keyboard.button(text="Скрыть реф.ссылку",callback_data=BotWorker(action="hide_ref_link",bot_username=bot_username))
    return keyboard.as_markup()

def profile_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🧾Отправить чек",callback_data=BotWorker(action="send_check"))
    keyboard.button(text="🔄Поменять тег",callback_data=BotWorker(action="change_tag"))
    keyboard.button(text="💰Поменять кошелек",callback_data=BotWorker(action="change_wallet"))
    return keyboard.adjust(2).as_markup()
    
def back_profile_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️Назад",callback_data=BotWorker(action="back_profile"))
    return keyboard.as_markup()