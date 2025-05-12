from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from utils.bot_state import UserState
from keyboards.reply import main_menu
from aiogram.fsm.context import FSMContext
command_router = Router()


@command_router.message(CommandStart())
async def cmd_start(message: Message,state:FSMContext) -> None:
    await message.answer_sticker("CAACAgIAAxkBAAEObXhoG31-0ExU21Op-Uq0Fge3hyvJNgACOXMAAlJGGEvAgeYEhpsRcDYE",
                                 reply_markup=main_menu())
    await message.answer(("💼 Профиль\n"
                          f"┣ ID: ({message.from_user.id}\n"
                          f"┣ Username: @{message.from_user.username}\n"
                          "┗ Ранг: Low\n\n"
                          "〽️ Личная статистика\n"
                          "┣ Сумма профитов: 0 RUB\n"
                          "┗ Количество профитов: 0\n\n"
                          "🎭 Информация\n"
                          "┣ Тег в выплатах: отсутствует\n"
                          "┣ Статус: Воркер\n"
                          "┗ В команде: 5 дн.\n"))
    await state.set_state(UserState.main_menu)

