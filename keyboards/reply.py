from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.menu_enum import MainMenuEnum


def main_menu() -> ReplyKeyboardBuilder:
    """Создает клавиатуру главного меню с кнопками 'Профиль', 'Статистика' и 'Выход'."""
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=MainMenuEnum.PROFILE.value),
        KeyboardButton(text=MainMenuEnum.INFORMATION.value),
        KeyboardButton(text=MainMenuEnum.TRADE.value),
        KeyboardButton(text=MainMenuEnum.SHOP.value),
        KeyboardButton(text=MainMenuEnum.ESCORT.value),
        KeyboardButton(text=MainMenuEnum.ABOUT_PROJECT.value),
    )
    return keyboard.adjust(2, 3, 1).as_markup(resize_keyboard=True)